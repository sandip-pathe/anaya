from pathlib import Path

from anaya.engine.orchestrator import ScanOrchestrator
from anaya.engine.rule_loader import load_rule_pack


def test_dirty_fixture_triggers_secret_rules():
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))
    summary = ScanOrchestrator([pack]).scan_paths(
        [Path("tests/fixtures/python/dirty/hardcoded_secret.py")]
    )

    assert summary.total_violations >= 4
    assert summary.overall_status == "FAIL"


def test_clean_fixture_has_no_findings():
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))
    summary = ScanOrchestrator([pack]).scan_paths(
        [Path("tests/fixtures/python/clean/proper_secrets.py")]
    )

    assert summary.total_violations == 0
    assert summary.overall_status == "PASS"
