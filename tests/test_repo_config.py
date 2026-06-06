from pathlib import Path

import pytest

from anaya.engine.repo_config import RepositoryConfigError, find_config, load_repository_config


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
    assert config.llm.enabled is False


def test_load_repository_config_enables_llm_only_when_requested(tmp_path: Path):
    config_path = tmp_path / "anaya.yml"
    config_path.write_text(
        "\n".join(
            [
                "packs:",
                "  - generic/secrets-detection",
                "llm:",
                "  enabled: true",
                "",
            ]
        ),
        encoding="utf-8",
    )

    config = load_repository_config(config_path)

    assert config.llm.enabled is True


def test_find_config_walks_parent_dirs(tmp_path: Path):
    config_path = tmp_path / "anaya.yml"
    nested = tmp_path / "src" / "pkg"
    nested.mkdir(parents=True)
    config_path.write_text("packs:\n  - generic/secrets-detection\n", encoding="utf-8")

    assert find_config(nested) == config_path


def test_repository_config_rejects_invalid_threshold(tmp_path: Path):
    config_path = tmp_path / "anaya.yml"
    config_path.write_text(
        "packs:\n  - generic/secrets-detection\nthresholds:\n  fail_on: EXTREME\n",
        encoding="utf-8",
    )

    with pytest.raises(RepositoryConfigError, match="thresholds.fail_on"):
        load_repository_config(config_path)


def test_repository_config_rejects_unknown_pack(tmp_path: Path):
    config_path = tmp_path / "anaya.yml"
    config_path.write_text("packs:\n  - missing/pack\n", encoding="utf-8")

    with pytest.raises(RepositoryConfigError, match="unknown pack"):
        load_repository_config(config_path)


def test_repository_config_rejects_invalid_scan_mode(tmp_path: Path):
    config_path = tmp_path / "anaya.yml"
    config_path.write_text(
        "packs:\n  - generic/secrets-detection\nscan:\n  mode: everything\n",
        encoding="utf-8",
    )

    with pytest.raises(RepositoryConfigError, match="scan.mode"):
        load_repository_config(config_path)


def test_repository_config_rejects_unknown_ignored_rule(tmp_path: Path):
    config_path = tmp_path / "anaya.yml"
    config_path.write_text(
        "\n".join(
            [
                "packs:",
                "  - generic/secrets-detection",
                "ignore:",
                "  rules:",
                "    - ANAYA-DOES-NOT-EXIST",
                "",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(RepositoryConfigError, match="ignore.rules"):
        load_repository_config(config_path)


def test_repository_config_rejects_non_boolean_llm_enabled(tmp_path: Path):
    config_path = tmp_path / "anaya.yml"
    config_path.write_text(
        "packs:\n  - generic/secrets-detection\nllm:\n  enabled: sometimes\n",
        encoding="utf-8",
    )

    with pytest.raises(RepositoryConfigError, match="llm.enabled"):
        load_repository_config(config_path)
