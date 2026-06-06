from pathlib import Path

from anaya.engine.orchestrator import ScanOrchestrator
from anaya.engine.repo_config import DEFAULT_PACKS
from anaya.engine.rule_loader import load_rule_pack


def test_default_generic_packs_load():
    packs = [
        load_rule_pack(Path("anaya/packs").joinpath(*pack_id.split("/")).with_suffix(".yml"))
        for pack_id in DEFAULT_PACKS
    ]

    assert len(packs) == 4
    assert sum(len(pack.rules) for pack in packs) == 16


def test_appsec_and_pii_fixture_triggers_multiple_packs():
    packs = [
        load_rule_pack(Path("anaya/packs").joinpath(*pack_id.split("/")).with_suffix(".yml"))
        for pack_id in DEFAULT_PACKS
    ]
    summary = ScanOrchestrator(packs).scan_paths(
        [Path("tests/fixtures/python/dirty/appsec_and_pii.py")]
    )
    rule_ids = {
        violation.rule_id
        for result in summary.results
        for violation in result.violations
    }

    assert "ANAYA-OWASP-001" in rule_ids
    assert "ANAYA-OWASP-002" in rule_ids
    assert "ANAYA-OWASP-004" in rule_ids
    assert "ANAYA-PII-001" in rule_ids
    assert "ANAYA-TLS-001" in rule_ids
    assert "ANAYA-TLS-002" in rule_ids
