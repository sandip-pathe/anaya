from pathlib import Path

from anaya.engine.orchestrator import ScanOrchestrator, resolve_pack_identifier
from anaya.engine.rule_loader import load_rule_pack, validate_rule_pack


PACK_PATH = Path("anaya/packs/india/dpdp-privacy.yml")


def test_india_dpdp_pack_loads_and_resolves_by_id():
    pack = load_rule_pack(PACK_PATH)

    assert pack.id == "india/dpdp-privacy"
    assert pack.version == "0.1.0"
    assert len(pack.rules) == 5
    assert resolve_pack_identifier("india/dpdp-privacy").resolve() == PACK_PATH.resolve()
    assert validate_rule_pack(PACK_PATH) == []


def test_india_dpdp_pack_detects_converted_rule_ids(tmp_path: Path):
    source = tmp_path / "india_dpdp_dirty.py"
    source.write_text(
        "\n".join(
            [
                'logger.info("aadhaar number: %s", aadhaar)',
                'password = "supersecret"',
                'requests.get("https://bank.example/api", verify=False)',
                'return jsonify({"email": email, "card_number": card_number})',
                'DB_HOST = "prod.db.example.com"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    pack = load_rule_pack(PACK_PATH)

    summary = ScanOrchestrator([pack]).scan_paths([source])
    rule_ids = {
        violation.rule_id
        for result in summary.results
        for violation in result.violations
    }

    assert rule_ids == {
        "DPDP-DATA-001",
        "DPDP-DATA-002",
        "DPDP-DATA-003",
        "DPDP-DATA-004",
        "DPDP-DATA-005",
    }


def test_india_dpdp_pack_clean_fixture_passes(tmp_path: Path):
    source = tmp_path / "india_dpdp_clean.py"
    source.write_text(
        "\n".join(
            [
                'logger.info("customer record updated")',
                'password = os.getenv("DB_PASSWORD")',
                'requests.get("https://bank.example/api", verify=True)',
                'return jsonify({"status": "ok"})',
                'DB_HOST = os.getenv("DB_HOST")',
                "",
            ]
        ),
        encoding="utf-8",
    )
    pack = load_rule_pack(PACK_PATH)

    summary = ScanOrchestrator([pack]).scan_paths([source])

    assert summary.total_violations == 0
    assert summary.overall_status == "PASS"
