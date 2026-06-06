from pathlib import Path
import subprocess

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


def test_scan_diff_uses_changed_files(tmp_path: Path):
    runner = CliRunner()
    source = tmp_path / "source.py"

    subprocess.run(["git", "init", "-b", "main"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    source.write_text("print('clean')\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=tmp_path, check=True, capture_output=True)
    source.write_text('api_key = "sk_live_1234567890abcdef"\n', encoding="utf-8")

    result = runner.invoke(app, ["scan", str(tmp_path), "--no-config", "--diff", "HEAD"])

    assert result.exit_code == 1
    assert "ANAYA-SEC-001" in result.output


def test_scan_config_resolves_custom_pack_relative_to_config(tmp_path: Path):
    runner = CliRunner()
    pack_dir = tmp_path / "packs"
    pack_dir.mkdir()
    pack_path = pack_dir / "custom.yml"
    config_path = tmp_path / "anaya.yml"
    source_path = tmp_path / "service.py"

    pack_path.write_text(
        "\n".join(
            [
                "pack:",
                '  id: "custom/internal-policy"',
                '  version: "1.0.0"',
                '  name: "Internal Policy"',
                '  description: "User-authored policy pack"',
                "rules:",
                '  - id: "CUSTOM-001"',
                '    name: "No Debug Payment Bypass"',
                '    description: "Debug payment bypass must not be enabled."',
                "    type: pattern",
                "    severity: HIGH",
                "    languages: [python]",
                "    patterns:",
                "      - regex: 'debug_payment_bypass\\s*=\\s*True'",
                '    message: "Debug payment bypass enabled at line {line}."',
                '    fix_hint: "Remove the bypass flag."',
                "    tags: [custom]",
                "",
            ]
        ),
        encoding="utf-8",
    )
    config_path.write_text(
        "packs:\n  - packs/custom.yml\nthresholds:\n  fail_on: HIGH\n",
        encoding="utf-8",
    )
    source_path.write_text("debug_payment_bypass = True\n", encoding="utf-8")

    result = runner.invoke(app, ["scan", str(tmp_path), "--config", str(config_path)])

    assert result.exit_code == 1
    assert "CUSTOM-001" in result.output
