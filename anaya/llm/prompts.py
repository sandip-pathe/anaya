"""Prompt construction for optional LLM-backed policy rules."""

from __future__ import annotations

from anaya.engine.models import Rule
from anaya.engine.scanners.pattern import detect_language


SYSTEM_PROMPT = """You are Anaya's optional compliance judge.
You review untrusted source code against one policy rule.
Return only JSON matching the provided schema.
Do not invent findings. If the code does not clearly violate the rule, return PASS.
Prefer deterministic evidence in the supplied code over speculation."""


JUDGE_RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "status": {"type": "string", "enum": ["PASS", "WARN", "FAIL"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reason": {"type": "string"},
        "line_number": {"type": ["integer", "null"], "minimum": 1},
    },
    "required": ["status", "confidence", "reason", "line_number"],
}


def build_judge_input(
    *,
    rule: Rule,
    file_path: str,
    scope_kind: str,
    scope_name: str,
    scope_start_line: int,
    scope_end_line: int,
    source: str,
) -> list[dict[str, object]]:
    """Build Responses API input for one bounded policy-judging task."""

    language = detect_language(file_path) or "text"
    policy_prompt = str(rule.raw.get("llm", {}).get("prompt", ""))
    user_prompt = "\n".join(
        [
            f"Rule ID: {rule.id}",
            f"Rule name: {rule.name}",
            f"Rule severity: {rule.severity}",
            f"Rule description: {rule.description}",
            f"Policy prompt: {policy_prompt}",
            f"File: {file_path}",
            f"Scope: {scope_kind} {scope_name}",
            f"Lines: {scope_start_line}-{scope_end_line}",
            "",
            "Source:",
            f"```{language}",
            source,
            "```",
            "",
            "Return PASS when there is no clear policy issue.",
            "Return WARN only for plausible policy issues that need human review.",
            "Return FAIL only for clear violations supported by the supplied source.",
        ]
    )
    return [
        {
            "role": "user",
            "content": [{"type": "input_text", "text": user_prompt}],
        }
    ]
