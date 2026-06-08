from pathlib import Path

import pytest

from anaya.engine.orchestrator import ScanOrchestrator
from anaya.engine.repo_config import DEFAULT_PACKS
from anaya.engine.rule_loader import load_rule_pack


def _load_default_packs():
    return [
        load_rule_pack(Path("anaya/packs").joinpath(*pack_id.split("/")).with_suffix(".yml"))
        for pack_id in DEFAULT_PACKS
    ]


PYTHON_DIRTY_RULES = {
    "ANAYA-AUDIT-001",
    "ANAYA-AUDIT-002",
    "ANAYA-AUDIT-003",
    "ANAYA-OWASP-001",
    "ANAYA-OWASP-002",
    "ANAYA-OWASP-003",
    "ANAYA-OWASP-004",
    "ANAYA-OWASP-005",
    "ANAYA-OWASP-006",
    "ANAYA-OWASP-007",
    "ANAYA-OWASP-008",
    "ANAYA-PII-001",
    "ANAYA-PII-002",
    "ANAYA-PII-003",
    "ANAYA-PII-004",
    "ANAYA-PII-005",
    "ANAYA-SEC-001",
    "ANAYA-SEC-002",
    "ANAYA-SEC-003",
    "ANAYA-SEC-006",
    "ANAYA-TLS-001",
    "ANAYA-TLS-002",
    "ANAYA-TLS-003",
    "ANAYA-TLS-004",
}


JAVASCRIPT_DIRTY_RULES = PYTHON_DIRTY_RULES - {"ANAYA-OWASP-004"}


def test_default_generic_packs_load():
    packs = _load_default_packs()

    assert len(packs) == 5
    assert sum(len(pack.rules) for pack in packs) == 29


def test_appsec_and_pii_fixture_triggers_multiple_packs():
    packs = _load_default_packs()
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


@pytest.mark.parametrize(
    ("fixture", "expected_rule_ids"),
    [
        (Path("tests/fixtures/python/dirty/security_matrix.py"), PYTHON_DIRTY_RULES),
        (Path("tests/fixtures/javascript/dirty/security_matrix.js"), JAVASCRIPT_DIRTY_RULES),
    ],
)
def test_dirty_fixture_matrix_matches_expected_rule_ids(
    fixture: Path,
    expected_rule_ids: set[str],
):
    summary = ScanOrchestrator(_load_default_packs()).scan_paths([fixture])
    rule_ids = {
        violation.rule_id
        for result in summary.results
        for violation in result.violations
    }

    assert rule_ids == expected_rule_ids


def test_provider_secret_patterns_detect_runtime_generated_values(tmp_path: Path):
    source = tmp_path / "provider_secrets.py"
    aws_key = "AKIA" + "ABCDEFGHIJKLMNOP"
    private_key_header = "-----BEGIN " + "RSA PRIVATE KEY-----"
    source.write_text(
        "\n".join(
            [
                f'aws_access_key = "{aws_key}"',
                f'private_key_header = "{private_key_header}"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))

    summary = ScanOrchestrator([pack]).scan_paths([source])
    rule_ids = {
        violation.rule_id
        for result in summary.results
        for violation in result.violations
    }

    assert {"ANAYA-SEC-004", "ANAYA-SEC-005"} <= rule_ids


@pytest.mark.parametrize(
    "fixture",
    [
        Path("tests/fixtures/python/clean/security_matrix.py"),
        Path("tests/fixtures/python/clean/audited_flows.py"),
        Path("tests/fixtures/javascript/clean/security_matrix.js"),
        Path("tests/fixtures/python/edge/suppressions.py"),
    ],
)
def test_clean_and_edge_fixtures_have_no_findings(fixture: Path):
    summary = ScanOrchestrator(_load_default_packs()).scan_paths([fixture])

    assert summary.total_violations == 0
