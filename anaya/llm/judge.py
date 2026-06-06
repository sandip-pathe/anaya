"""Optional OpenAI-backed policy judge."""

from __future__ import annotations

import ast
from collections.abc import Callable
from dataclasses import dataclass
import json
from time import sleep
from typing import Any, Protocol

from anaya.config import Settings
from anaya.engine.models import Rule, Violation
from anaya.engine.scanners.pattern import detect_language
from anaya.llm.prompts import JUDGE_RESPONSE_SCHEMA, SYSTEM_PROMPT, build_judge_input


MAX_OUTPUT_TOKENS = 300
MAX_TIMEOUT_SECONDS = 10.0
MAX_TEMPERATURE = 0.1
RETRYABLE_STATUS_CODES = {429}


@dataclass(frozen=True)
class LlmDecision:
    """Structured output returned by the LLM judge."""

    status: str
    confidence: float
    reason: str
    line_number: int | None


@dataclass(frozen=True)
class LlmScope:
    """One bounded unit of code sent to the judge."""

    kind: str
    name: str
    source: str
    start_line: int
    end_line: int


@dataclass(frozen=True)
class LlmScanOutcome:
    """LLM scan result plus non-blocking warnings."""

    violations: tuple[Violation, ...] = ()
    warnings: tuple[str, ...] = ()


class LlmJudgeProtocol(Protocol):
    """Protocol used by the orchestrator and tests."""

    def scan_file_content(
        self,
        file_path: str,
        content: str,
        rules: list[Rule],
    ) -> LlmScanOutcome:
        """Scan one file with LLM-backed rules."""


class LlmJudgeError(RuntimeError):
    """Raised when one LLM judgment cannot be trusted."""


class LlmJudgeUnavailable(RuntimeError):
    """Raised when OpenAI judging was requested but cannot be configured."""


class OpenAIJudge:
    """Run opt-in LLM rules through OpenAI with strict safety defaults."""

    def __init__(
        self,
        *,
        client: Any,
        model: str,
        max_tokens: int = MAX_OUTPUT_TOKENS,
        temperature: float = MAX_TEMPERATURE,
        timeout_seconds: float = MAX_TIMEOUT_SECONDS,
        sleeper: Callable[[float], None] = sleep,
    ):
        self.client = client
        self.model = model
        self.max_tokens = max(1, min(max_tokens, MAX_OUTPUT_TOKENS))
        self.temperature = max(0.0, min(temperature, MAX_TEMPERATURE))
        self.timeout_seconds = max(0.1, min(timeout_seconds, MAX_TIMEOUT_SECONDS))
        self.sleeper = sleeper

    def scan_file_content(
        self,
        file_path: str,
        content: str,
        rules: list[Rule],
    ) -> LlmScanOutcome:
        """Judge one file with active LLM rules."""

        language = detect_language(file_path)
        if language is None:
            return LlmScanOutcome()

        violations: list[Violation] = []
        warnings: list[str] = []
        lines = content.splitlines()
        for rule in rules:
            if not _rule_applies(rule, language):
                continue
            scopes, scope_warnings = _scopes_for_rule(rule, file_path, content)
            warnings.extend(scope_warnings)
            for scope in scopes:
                try:
                    decision = self._judge(rule, file_path, scope)
                except LlmJudgeError as exc:
                    warnings.append(f"{rule.id} skipped for {file_path}: {exc}")
                    continue
                if decision.status == "PASS":
                    continue
                violations.append(_build_violation(rule, file_path, decision, scope, lines))

        return LlmScanOutcome(
            violations=tuple(sorted(violations, key=lambda item: (item.line_number, item.rule_id))),
            warnings=tuple(_dedupe(warnings)),
        )

    def _judge(self, rule: Rule, file_path: str, scope: LlmScope) -> LlmDecision:
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                response = self.client.responses.create(
                    model=self.model,
                    instructions=SYSTEM_PROMPT,
                    input=build_judge_input(
                        rule=rule,
                        file_path=file_path,
                        scope_kind=scope.kind,
                        scope_name=scope.name,
                        scope_start_line=scope.start_line,
                        scope_end_line=scope.end_line,
                        source=scope.source,
                    ),
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                    timeout=self.timeout_seconds,
                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "anaya_llm_judge",
                            "strict": True,
                            "schema": JUDGE_RESPONSE_SCHEMA,
                        }
                    },
                )
                return _parse_decision(_extract_output_text(response))
            except Exception as exc:
                last_error = exc
                if attempt == 0 and _is_retryable(exc):
                    self.sleeper(1.0)
                    continue
                break
        raise LlmJudgeError(_error_message(last_error))


def create_openai_judge(settings: Settings) -> tuple[OpenAIJudge | None, tuple[str, ...]]:
    """Create an OpenAI judge, returning warnings instead of raising configuration errors."""

    if not settings.openai_api_key:
        return None, ("LLM rules enabled but ANAYA_OPENAI_API_KEY is not set; skipping LLM rules.",)
    try:
        from openai import OpenAI
    except ImportError:
        return None, ("LLM rules enabled but the optional 'openai' dependency is not installed.",)

    client = OpenAI(
        api_key=settings.openai_api_key,
        timeout=max(0.1, min(settings.openai_timeout_seconds, MAX_TIMEOUT_SECONDS)),
        max_retries=0,
    )
    return (
        OpenAIJudge(
            client=client,
            model=settings.openai_model,
            max_tokens=settings.openai_max_tokens,
            temperature=settings.openai_temperature,
            timeout_seconds=settings.openai_timeout_seconds,
        ),
        (),
    )


def _rule_applies(rule: Rule, language: str) -> bool:
    return (
        rule.enabled
        and rule.type == "llm"
        and (not rule.languages or language in rule.languages)
    )


def _scopes_for_rule(rule: Rule, file_path: str, content: str) -> tuple[list[LlmScope], list[str]]:
    scope = str(rule.raw.get("llm", {}).get("scope", "file"))
    if scope == "file":
        line_count = max(len(content.splitlines()), 1)
        return [LlmScope("file", file_path, content, 1, line_count)], []
    if scope == "function" and detect_language(file_path) == "python":
        return _python_function_scopes(rule.id, file_path, content)
    if scope == "function":
        return [], [f"{rule.id} skipped for {file_path}: function scope currently requires Python."]
    return [], [f"{rule.id} skipped for {file_path}: unsupported LLM scope {scope!r}."]


def _python_function_scopes(
    rule_id: str,
    file_path: str,
    content: str,
) -> tuple[list[LlmScope], list[str]]:
    try:
        tree = ast.parse(content)
    except SyntaxError as exc:
        line = exc.lineno or 1
        return [], [f"{rule_id} skipped for {file_path}: Python parse failed near line {line}."]

    lines = content.splitlines()
    scopes: list[LlmScope] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        start_line = node.lineno
        end_line = getattr(node, "end_lineno", None) or start_line
        source = "\n".join(lines[start_line - 1 : end_line])
        scopes.append(LlmScope("function", node.name, source, start_line, end_line))
    return sorted(scopes, key=lambda item: (item.start_line, item.name)), []


def _parse_decision(raw_text: str) -> LlmDecision:
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise LlmJudgeError("OpenAI returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise LlmJudgeError("OpenAI returned a non-object JSON value")

    status = str(payload.get("status", "")).upper()
    if status not in {"PASS", "WARN", "FAIL"}:
        raise LlmJudgeError("OpenAI returned an invalid status")

    try:
        confidence = float(payload["confidence"])
    except (KeyError, TypeError, ValueError) as exc:
        raise LlmJudgeError("OpenAI returned an invalid confidence") from exc
    if not 0 <= confidence <= 1:
        raise LlmJudgeError("OpenAI returned confidence outside 0..1")

    reason = str(payload.get("reason", "")).strip()
    if not reason:
        raise LlmJudgeError("OpenAI returned an empty reason")

    raw_line = payload.get("line_number")
    if raw_line is None:
        line_number = None
    elif isinstance(raw_line, int) and raw_line > 0:
        line_number = raw_line
    else:
        raise LlmJudgeError("OpenAI returned an invalid line_number")

    return LlmDecision(status=status, confidence=confidence, reason=reason, line_number=line_number)


def _extract_output_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text
    if isinstance(response, dict):
        output_text = response.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text
    raise LlmJudgeError("OpenAI response did not include text output")


def _build_violation(
    rule: Rule,
    file_path: str,
    decision: LlmDecision,
    scope: LlmScope,
    lines: list[str],
) -> Violation:
    max_line = max(len(lines), 1)
    line_number = decision.line_number or scope.start_line
    if line_number < scope.start_line or line_number > scope.end_line:
        line_number = scope.start_line
    line_number = max(1, min(line_number, max_line))
    snippet = lines[line_number - 1].rstrip() if lines else ""
    return Violation(
        rule_id=rule.id,
        rule_name=rule.name,
        severity=rule.severity,
        file_path=file_path,
        line_number=line_number,
        end_line=None,
        column=1,
        snippet=snippet,
        message=_render_template(
            rule.message,
            {
                "line": line_number,
                "file": file_path,
                "rule": rule.id,
                "status": decision.status,
                "confidence": f"{decision.confidence:.2f}",
                "reason": decision.reason,
                "scope": scope.name,
            },
        ),
        fix_hint=rule.fix_hint,
        references=rule.references,
        pack_id=rule.pack_id,
        confidence=decision.confidence,
    )


def _render_template(template: str, values: dict[str, object]) -> str:
    try:
        return template.format(**values)
    except (KeyError, ValueError):
        return template


def _is_retryable(exc: Exception) -> bool:
    status_code = getattr(exc, "status_code", None)
    if status_code in RETRYABLE_STATUS_CODES:
        return True
    if isinstance(status_code, int) and status_code >= 500:
        return True
    response = getattr(exc, "response", None)
    response_status = getattr(response, "status_code", None)
    return response_status in RETRYABLE_STATUS_CODES or (
        isinstance(response_status, int) and response_status >= 500
    )


def _error_message(exc: Exception | None) -> str:
    if exc is None:
        return "OpenAI judge failed"
    if isinstance(exc, LlmJudgeError):
        return str(exc)
    status_code = getattr(exc, "status_code", None)
    if status_code is not None:
        return f"OpenAI request failed with status {status_code}"
    return exc.__class__.__name__


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))
