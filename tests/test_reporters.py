from pathlib import Path
import json

from anaya.engine.orchestrator import ScanOrchestrator
from anaya.engine.rule_loader import load_rule_pack
from anaya.reporter.json_report import format_json
from anaya.reporter.sarif import format_sarif
from anaya.reporter.table import format_table


def _dirty_summary():
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))
    return ScanOrchestrator([pack]).scan_paths(
        [Path("tests/fixtures/python/dirty/hardcoded_secret.py")]
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


def test_sarif_report_contains_tool_and_results():
    rendered = format_sarif(_dirty_summary())
    payload = json.loads(rendered)
    run = payload["runs"][0]
    result = run["results"][0]
    rule = run["tool"]["driver"]["rules"][0]

    assert payload["version"] == "2.1.0"
    assert run["tool"]["driver"]["name"] == "Anaya"
    assert result["ruleId"] == "ANAYA-SEC-001"
    assert "\\" not in result["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
    assert rule["helpUri"].startswith("https://")
