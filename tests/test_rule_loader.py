from pathlib import Path

from anaya.engine.rule_loader import load_rule_pack, validate_rule_pack


def test_builtin_secrets_pack_loads():
    pack = load_rule_pack(Path("anaya/packs/generic/secrets-detection.yml"))

    assert pack.id == "generic/secrets-detection"
    assert len(pack.rules) == 6


def test_builtin_secrets_pack_validates():
    assert validate_rule_pack(Path("anaya/packs/generic/secrets-detection.yml")) == []
