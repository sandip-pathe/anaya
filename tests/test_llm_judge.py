from __future__ import annotations

import json
from pathlib import Path

from anaya.config import Settings
from anaya.engine.orchestrator import ScanOrchestrator
from anaya.engine.rule_loader import load_rule_pack
from anaya.llm.judge import OpenAIJudge, create_openai_judge


class RetryableError(Exception):
    status_code = 429


class FakeResponses:
    def __init__(self, *items: object):
        self.items = list(items)
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        item = self.items.pop(0)
        if isinstance(item, Exception):
            raise item
        return {"output_text": json.dumps(item)}


class FakeClient:
    def __init__(self, *items: object):
        self.responses = FakeResponses(*items)


def test_llm_rules_are_inert_without_a_configured_judge(tmp_path: Path):
    pack = load_rule_pack(_write_llm_pack(tmp_path))

    summary = ScanOrchestrator([pack]).scan_contents(
        [("src/payment.py", "def transfer():\n    pass\n")]
    )

    assert summary.rules_checked == 0
    assert summary.total_violations == 0
    assert summary.warnings == ()


def test_openai_judge_turns_structured_fail_into_violation(tmp_path: Path):
    pack = load_rule_pack(_write_llm_pack(tmp_path))
    client = FakeClient(
        {
            "status": "FAIL",
            "confidence": 0.82,
            "reason": "transfer function does not emit an audit event",
            "line_number": 2,
        }
    )
    judge = OpenAIJudge(
        client=client,
        model="gpt-test",
        max_tokens=999,
        temperature=1,
        timeout_seconds=60,
        sleeper=lambda _: None,
    )

    summary = ScanOrchestrator([pack], llm_judge=judge).scan_contents(
        [("src/payment.py", "def transfer():\n    pass\n")]
    )

    violation = summary.results[0].violations[0]
    call = client.responses.calls[0]
    assert summary.rules_checked == 1
    assert summary.total_violations == 1
    assert violation.rule_id == "CUSTOM-LLM-001"
    assert violation.line_number == 2
    assert violation.confidence == 0.82
    assert "does not emit an audit event" in violation.message
    assert call["max_output_tokens"] == 300
    assert call["temperature"] == 0.1
    assert call["timeout"] == 10.0
    assert call["text"]["format"]["type"] == "json_schema"


def test_openai_judge_retries_one_retryable_error(tmp_path: Path):
    pack = load_rule_pack(_write_llm_pack(tmp_path))
    client = FakeClient(
        RetryableError("rate limited"),
        {
            "status": "PASS",
            "confidence": 0.91,
            "reason": "audit event is present",
            "line_number": None,
        },
    )
    judge = OpenAIJudge(client=client, model="gpt-test", sleeper=lambda _: None)

    summary = ScanOrchestrator([pack], llm_judge=judge).scan_contents(
        [("src/payment.py", "def transfer():\n    audit_log()\n")]
    )

    assert len(client.responses.calls) == 2
    assert summary.total_violations == 0
    assert summary.warnings == ()


def test_openai_judge_bad_output_skips_with_warning(tmp_path: Path):
    pack = load_rule_pack(_write_llm_pack(tmp_path))
    client = FakeClient(
        {
            "status": "MAYBE",
            "confidence": 0.9,
            "reason": "unclear",
            "line_number": None,
        }
    )
    judge = OpenAIJudge(client=client, model="gpt-test", sleeper=lambda _: None)

    summary = ScanOrchestrator([pack], llm_judge=judge).scan_contents(
        [("src/payment.py", "def transfer():\n    pass\n")]
    )

    assert summary.total_violations == 0
    assert "invalid status" in summary.warnings[0]


def test_function_scope_sends_python_functions_not_lines(tmp_path: Path):
    pack = load_rule_pack(_write_llm_pack(tmp_path, scope="function"))
    client = FakeClient(
        {"status": "PASS", "confidence": 0.9, "reason": "ok", "line_number": None},
        {"status": "PASS", "confidence": 0.9, "reason": "ok", "line_number": None},
    )
    judge = OpenAIJudge(client=client, model="gpt-test", sleeper=lambda _: None)

    ScanOrchestrator([pack], llm_judge=judge).scan_contents(
        [
            (
                "src/payment.py",
                "def transfer():\n    pass\n\n\ndef refund():\n    pass\n",
            )
        ]
    )

    prompts = [
        call["input"][0]["content"][0]["text"]
        for call in client.responses.calls
    ]
    assert len(prompts) == 2
    assert "Scope: function transfer" in prompts[0]
    assert "Scope: function refund" in prompts[1]


def test_create_openai_judge_missing_key_returns_warning():
    judge, warnings = create_openai_judge(Settings(openai_api_key=None))

    assert judge is None
    assert "ANAYA_OPENAI_API_KEY" in warnings[0]


def _write_llm_pack(tmp_path: Path, *, scope: str = "file") -> Path:
    pack_path = tmp_path / "llm-pack.yml"
    pack_path.write_text(
        "\n".join(
            [
                "pack:",
                '  id: "custom/llm-audit"',
                '  version: "1.0.0"',
                '  name: "LLM Audit"',
                '  description: "User-authored LLM rule pack"',
                "rules:",
                '  - id: "CUSTOM-LLM-001"',
                '    name: "Audit Reasoning"',
                '    description: "Use LLM reasoning for ambiguous audit requirements."',
                "    type: llm",
                "    severity: HIGH",
                "    languages: [python]",
                "    llm:",
                f"      scope: {scope}",
                '      prompt: "Decide whether this code clearly emits audit evidence."',
                '    message: "OpenAI judge returned {status}: {reason}"',
                '    fix_hint: "Add explicit audit evidence or disable this opt-in rule."',
                "",
            ]
        ),
        encoding="utf-8",
    )
    return pack_path
