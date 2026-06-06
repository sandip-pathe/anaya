from pathlib import Path

from anaya.engine.orchestrator import ScanOrchestrator
from anaya.engine.rule_loader import load_rule_pack


def test_python_ast_audit_rules_find_missing_audit_calls():
    pack = load_rule_pack(Path("anaya/packs/generic/audit-logging.yml"))
    summary = ScanOrchestrator([pack]).scan_paths(
        [Path("tests/fixtures/python/dirty/missing_audit.py")]
    )
    rule_ids = {
        violation.rule_id
        for result in summary.results
        for violation in result.violations
    }

    assert rule_ids == {"ANAYA-AUDIT-004", "ANAYA-AUDIT-005", "ANAYA-AUDIT-006"}
    assert summary.total_violations == 3


def test_python_ast_audit_rules_pass_audited_flows():
    pack = load_rule_pack(Path("anaya/packs/generic/audit-logging.yml"))
    summary = ScanOrchestrator([pack]).scan_paths(
        [Path("tests/fixtures/python/clean/audited_flows.py")]
    )

    assert summary.total_violations == 0
