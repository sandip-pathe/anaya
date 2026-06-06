from pathlib import Path

from anaya.engine.repo_config import find_config, load_repository_config


def test_load_repository_config_with_pack_mappings(tmp_path: Path):
    config_path = tmp_path / "anaya.yml"
    config_path.write_text(
        "\n".join(
            [
                'version: "1"',
                "packs:",
                "  - id: generic/secrets-detection",
                "thresholds:",
                "  fail_on: HIGH",
                "  warn_on: MEDIUM",
                "ignore:",
                "  paths:",
                '    - "tests/**"',
                "  rules:",
                "    - ANAYA-SEC-001",
                "",
            ]
        ),
        encoding="utf-8",
    )

    config = load_repository_config(config_path)

    assert config.packs == ("generic/secrets-detection",)
    assert config.thresholds.fail_on == "HIGH"
    assert config.thresholds.warn_on == "MEDIUM"
    assert config.ignore.paths == ("tests/**",)
    assert config.ignore.rules == ("ANAYA-SEC-001",)


def test_find_config_walks_parent_dirs(tmp_path: Path):
    config_path = tmp_path / "anaya.yml"
    nested = tmp_path / "src" / "pkg"
    nested.mkdir(parents=True)
    config_path.write_text("packs:\n  - generic/secrets-detection\n", encoding="utf-8")

    assert find_config(nested) == config_path
