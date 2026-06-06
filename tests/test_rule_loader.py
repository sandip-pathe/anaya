from pathlib import Path

import pytest

from anaya.engine.rule_loader import RulePackError
from anaya.engine.rule_loader import load_rule_pack, validate_rule_pack


def test_builtin_secrets_pack_loads():
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))

    assert pack.id == "generic/secrets-detection"
    assert len(pack.rules) == 6


def test_builtin_secrets_pack_validates():
    assert validate_rule_pack(Path("anaya/packs/generic/secrets-detection.yml")) == []


def test_rule_pack_rejects_duplicate_rule_ids(tmp_path: Path):
    pack_path = tmp_path / "bad.yml"
    pack_path.write_text(
        "\n".join(
            [
                "pack:",
                '  id: "custom/bad"',
                '  version: "1.0.0"',
                "rules:",
                '  - id: "CUSTOM-001"',
                '    name: "One"',
                '    description: "One"',
                "    type: pattern",
                "    severity: HIGH",
                "    languages: [python]",
                "    patterns:",
                "      - regex: 'foo'",
                '    message: "foo"',
                '    fix_hint: "fix"',
                '  - id: "CUSTOM-001"',
                '    name: "Two"',
                '    description: "Two"',
                "    type: pattern",
                "    severity: HIGH",
                "    languages: [python]",
                "    patterns:",
                "      - regex: 'bar'",
                '    message: "bar"',
                '    fix_hint: "fix"',
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(RulePackError, match="duplicate rule"):
        load_rule_pack(pack_path)


def test_rule_pack_rejects_unsupported_language(tmp_path: Path):
    pack_path = tmp_path / "bad-language.yml"
    pack_path.write_text(
        "\n".join(
            [
                "pack:",
                '  id: "custom/bad-language"',
                '  version: "1.0.0"',
                "rules:",
                '  - id: "CUSTOM-001"',
                '    name: "Unsupported"',
                '    description: "Unsupported"',
                "    type: pattern",
                "    severity: HIGH",
                "    languages: [cobol]",
                "    patterns:",
                "      - regex: 'foo'",
                '    message: "foo"',
                '    fix_hint: "fix"',
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(RulePackError, match="unsupported language"):
        load_rule_pack(pack_path)


def test_rule_pack_rejects_non_semver_version(tmp_path: Path):
    pack_path = tmp_path / "bad-version.yml"
    pack_path.write_text("pack:\n  id: custom/bad\n  version: soon\nrules:\n  - nope\n", encoding="utf-8")

    with pytest.raises(RulePackError, match="SemVer"):
        load_rule_pack(pack_path)


def test_rule_pack_rejects_invalid_ast_schema(tmp_path: Path):
    pack_path = tmp_path / "bad-ast.yml"
    pack_path.write_text(
        "\n".join(
            [
                "pack:",
                '  id: "custom/bad-ast"',
                '  version: "1.0.0"',
                "rules:",
                '  - id: "CUSTOM-AST-001"',
                '    name: "Bad AST"',
                '    description: "Bad AST"',
                "    type: ast",
                "    severity: HIGH",
                "    languages: [python]",
                "    ast:",
                "      node_type: class",
                "      name_matches: transfer",
                "      must_contain: [audit]",
                "      if_missing: flag",
                '    message: "missing audit"',
                '    fix_hint: "add audit"',
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(RulePackError, match="ast.node_type"):
        load_rule_pack(pack_path)
