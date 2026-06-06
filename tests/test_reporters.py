from pathlib import Path
import json

from jsonschema import validate

from anaya.engine.orchestrator import ScanOrchestrator
from anaya.engine.repo_config import DEFAULT_PACKS
from anaya.engine.rule_loader import load_rule_pack
from anaya.reporter.audit_json import format_audit_json
from anaya.reporter.check_run import build_check_run_payloads
from anaya.reporter.json_report import format_json
from anaya.reporter.pr_comment import format_pr_comment
from anaya.reporter.sarif import format_sarif
from anaya.reporter.table import format_table


SARIF_CONTRACT_SCHEMA = {
    "type": "object",
    "required": ["version", "$schema", "runs"],
    "properties": {
        "version": {"const": "2.1.0"},
        "runs": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["tool", "results"],
                "properties": {
                    "tool": {
                        "type": "object",
                        "required": ["driver"],
                        "properties": {
                            "driver": {
                                "type": "object",
                                "required": ["name", "version", "rules"],
                            }
                        },
                    },
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["ruleId", "level", "message", "locations"],
                        },
                    },
                },
            },
        },
    },
}


def _dirty_summary():
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))
    return ScanOrchestrator([pack]).scan_paths(
        [Path("tests/fixtures/python/dirty/hardcoded_secret.py")]
    )


def _matrix_summary():
    packs = [
        load_rule_pack(Path("anaya/packs").joinpath(*pack_id.split("/")).with_suffix(".yml"))
        for pack_id in DEFAULT_PACKS
    ]
    return ScanOrchestrator(packs).scan_paths(
        [
            Path("tests/fixtures/python/dirty/security_matrix.py"),
            Path("tests/fixtures/javascript/dirty/security_matrix.js"),
        ]
    )


def test_json_report_includes_summary_fields():
    rendered = format_json(_dirty_summary())
    payload = json.loads(rendered)

    assert payload["total_violations"] == 4
    assert payload["results"][0]["violations"][0]["rule_id"] == "ANAYA-SEC-001"


def test_table_report_includes_findings_and_fixes():
    rendered = format_table(_dirty_summary())

    assert "Anaya Policy Scan" in rendered
    assert "Rules checked:" in rendered
    assert "Pack versions:" in rendered
    assert "ANAYA-SEC-001" in rendered
    assert "Fix:" in rendered


def test_table_report_includes_no_findings_message():
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))
    summary = ScanOrchestrator([pack]).scan_paths(
        [Path("tests/fixtures/python/clean/proper_secrets.py")]
    )
    rendered = format_table(summary)

    assert "No findings." in rendered
    assert "Severity: none" in rendered


def test_sarif_report_contains_tool_and_results():
    rendered = format_sarif(_dirty_summary())
    payload = json.loads(rendered)
    run = payload["runs"][0]
    result = run["results"][0]
    rule = run["tool"]["driver"]["rules"][0]

    assert payload["version"] == "2.1.0"
    assert run["automationDetails"]["id"] == "anaya/default"
    assert run["invocations"][0]["executionSuccessful"] is True
    assert run["tool"]["driver"]["name"] == "Anaya"
    assert result["ruleId"] == "ANAYA-SEC-001"
    assert result["partialFingerprints"]["anaya/v1"]
    assert "\\" not in result["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
    assert rule["helpUri"].startswith("https://")
    validate(payload, SARIF_CONTRACT_SCHEMA)


def test_audit_json_report_groups_scan_metadata():
    payload = json.loads(format_audit_json(_dirty_summary()))

    assert payload["tool"]["name"] == "Anaya"
    assert payload["scan"]["pack_versions"] == {"generic/secrets-detection": "1.0.0"}
    assert payload["summary"]["total_violations"] == 4


def test_check_run_report_batches_annotations():
    payloads = build_check_run_payloads(_matrix_summary())

    assert len(payloads) == 2
    assert payloads[0]["conclusion"] == "failure"
    assert len(payloads[0]["output"]["annotations"]) == 50
    assert len(payloads[1]["output"]["annotations"]) > 0
    assert "total annotations" in payloads[1]["output"]["summary"]


def test_pr_comment_report_contains_markdown_summary():
    rendered = format_pr_comment(_dirty_summary())

    assert "## Anaya Policy Scan" in rendered
    assert "| Pack | Status | Findings |" in rendered
    assert "ANAYA-SEC-001" in rendered
