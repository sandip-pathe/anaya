from pathlib import Path

from typer.testing import CliRunner

from anaya.cli.main import app


def test_scan_output_creates_parent_directory(tmp_path: Path):
    runner = CliRunner()
    output_path = tmp_path / "reports" / "dirty.json"

    result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/python/dirty/hardcoded_secret.py",
            "--no-config",
            "--format",
            "json",
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 1
    assert output_path.exists()
    assert '"total_violations": 4' in output_path.read_text(encoding="utf-8")


def test_scan_uses_config_ignores(tmp_path: Path):
    fixture = Path("tests/fixtures/python/dirty/hardcoded_secret.py")
    config_path = tmp_path / "anaya.yml"
    config_path.write_text(
        "\n".join(
            [
                'version: "1"',
                "packs:",
                "  - id: generic/secrets-detection",
                "thresholds:",
                "  fail_on: CRITICAL",
                "  warn_on: HIGH",
                "ignore:",
                "  rules:",
                "    - ANAYA-SEC-001",
                "    - ANAYA-SEC-002",
                "    - ANAYA-SEC-003",
                "    - ANAYA-SEC-006",
                "",
            ]
        ),
        encoding="utf-8",
    )

    runner = CliRunner()
    result = runner.invoke(app, ["scan", str(fixture), "--config", str(config_path)])

    assert result.exit_code == 0
    assert "0 violation(s)" in result.output


def test_init_validate_and_list_commands(tmp_path: Path):
    runner = CliRunner()
    config_path = tmp_path / "anaya.yml"

    init_result = runner.invoke(app, ["init", "--path", str(config_path)])
    validate_result = runner.invoke(
        app,
        ["validate-pack", "anaya/packs/generic/secrets-detection.yml"],
    )
    list_result = runner.invoke(app, ["packs", "list"])

    assert init_result.exit_code == 0
    assert config_path.exists()
    assert validate_result.exit_code == 0
    assert "is valid" in validate_result.output
    assert list_result.exit_code == 0
    assert "generic/secrets-detection" in list_result.output


def test_scan_rejects_unknown_format():
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/python/clean/proper_secrets.py",
            "--no-config",
            "--format",
            "xml",
        ],
    )

    assert result.exit_code != 0
    assert "format must be one of" in result.output
