from pathlib import Path

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

    assert '"total_violations": 4' in rendered
    assert '"ANAYA-SEC-001"' in rendered


def test_table_report_includes_findings_and_fixes():
    rendered = format_table(_dirty_summary())

    assert "Anaya Policy Scan" in rendered
    assert "Rules checked:" in rendered
    assert "ANAYA-SEC-001" in rendered
    assert "Fix:" in rendered


def test_sarif_report_contains_tool_and_results():
    rendered = format_sarif(_dirty_summary())

    assert '"version": "2.1.0"' in rendered
    assert '"name": "Anaya"' in rendered
    assert '"ruleId": "ANAYA-SEC-001"' in rendered
