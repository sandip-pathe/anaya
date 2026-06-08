from pathlib import Path

from anaya.engine.orchestrator import ScanOrchestrator
from anaya.engine.repo_config import DEFAULT_PACKS
from anaya.engine.rule_loader import load_rule_pack


def test_summary_includes_metadata_and_skipped_files(tmp_path: Path):
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))
    source = tmp_path / "source.py"
    ignored = tmp_path / "ignored.py"
    unsupported = tmp_path / "notes.txt"
    binary = tmp_path / "binary.py"

    source.write_text('api_key = "anaya_test_secret_1234567890"\n', encoding="utf-8")
    ignored.write_text('api_key = "anaya_test_secret_1234567890"\n', encoding="utf-8")
    unsupported.write_text("hello\n", encoding="utf-8")
    binary.write_bytes(b"abc\x00def")

    summary = ScanOrchestrator([pack]).scan_paths(
        [tmp_path],
        ignore=(ignored.name,),
        config_path="anaya.yml",
    )

    assert summary.config_path == "anaya.yml"
    assert summary.rules_checked == len(pack.rules)
    assert summary.pack_versions == {"generic/secrets-detection": "1.0.0"}
    assert summary.skipped_files["ignored"] == 1
    assert summary.skipped_files["unsupported"] == 1
    assert summary.skipped_files["binary"] == 1
    assert summary.total_files == 1
    assert summary.total_violations == 1


def test_ignored_rules_reduce_rules_checked_and_findings():
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))
    summary = ScanOrchestrator([pack]).scan_paths(
        [Path("tests/fixtures/python/dirty/hardcoded_secret.py")],
        ignored_rules=("ANAYA-SEC-001", "ANAYA-SEC-002", "ANAYA-SEC-003", "ANAYA-SEC-006"),
    )

    assert summary.rules_checked == len(pack.rules) - 4
    assert summary.total_violations == 0


def test_scan_languages_filters_files_and_rules(tmp_path: Path):
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))
    source = tmp_path / "source.py"
    source.write_text('api_key = "anaya_test_secret_1234567890"\n', encoding="utf-8")

    summary = ScanOrchestrator([pack]).scan_paths([tmp_path], languages=("javascript",))

    assert summary.total_files == 0
    assert summary.total_violations == 0
    assert summary.rules_checked == len(pack.rules)
    assert summary.skipped_files["language_filtered"] == 1


def test_scan_languages_filters_rule_set(tmp_path: Path):
    pack = load_rule_pack(Path("anaya/packs/generic/owasp-top10.yml"))
    source = tmp_path / "source.rs"
    source.write_text("fn main() {}\n", encoding="utf-8")

    summary = ScanOrchestrator([pack]).scan_paths([source], languages=("rust",))

    assert summary.total_files == 1
    assert summary.rules_checked == 0
    assert summary.total_violations == 0


def test_pack_status_tracks_warns_even_after_overall_fail():
    packs = [
        load_rule_pack(Path("anaya/packs").joinpath(*pack_id.split("/")).with_suffix(".yml"))
        for pack_id in DEFAULT_PACKS
    ]
    summary = ScanOrchestrator(packs).scan_paths(
        [Path("tests/fixtures/python/dirty/security_matrix.py")]
    )

    assert summary.overall_status == "FAIL"
    assert summary.by_pack["generic/secrets-detection"]["status"] == "FAIL"
    assert summary.by_pack["generic/owasp-top10"]["status"] == "WARN"
    assert summary.by_pack["generic/audit-logging"]["status"] == "WARN"


def test_scan_contents_uses_repo_relative_paths():
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))
    summary = ScanOrchestrator([pack]).scan_contents(
        [("src/app.py", 'api_key = "anaya_test_secret_1234567890"\n')]
    )

    assert summary.total_violations == 1
    assert summary.results[0].file_path == "src/app.py"
    assert summary.results[0].violations[0].file_path == "src/app.py"
