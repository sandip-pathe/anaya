"""YAML rule pack loading and validation."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import yaml

from anaya.engine.models import RULE_TYPES, SEVERITY_ORDER, SUPPORTED_LANGUAGES, Rule, RulePack, RulePattern


SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


class RulePackError(ValueError):
    """Raised when a rule pack cannot be loaded or validated."""


def load_rule_pack(path: str | Path) -> RulePack:
    """Load a YAML rule pack into typed engine models."""

    pack_path = Path(path)
    if not pack_path.exists():
        raise RulePackError(f"Rule pack not found: {pack_path}")

    try:
        raw = yaml.safe_load(pack_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise RulePackError(f"Malformed YAML in {pack_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise RulePackError(f"Rule pack must be a YAML mapping: {pack_path}")

    pack_meta = _require_mapping(raw, "pack", pack_path)
    raw_rules = raw.get("rules")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise RulePackError(f"{pack_path}: rules must be a non-empty list")

    pack_id = _require_str(pack_meta, "id", pack_path)
    pack_version = _require_str(pack_meta, "version", pack_path)
    if not SEMVER_PATTERN.match(pack_version):
        raise RulePackError(f"{pack_path}: pack version must be SemVer, got {pack_version!r}")
    rules = tuple(_load_rule(item, pack_id, pack_version, pack_path) for item in raw_rules)
    rule_ids = [rule.id for rule in rules]
    duplicate_ids = sorted({rule_id for rule_id in rule_ids if rule_ids.count(rule_id) > 1})
    if duplicate_ids:
        raise RulePackError(f"{pack_path}: duplicate rule id(s): {', '.join(duplicate_ids)}")

    return RulePack(
        id=pack_id,
        version=pack_version,
        name=str(pack_meta.get("name", pack_id)),
        description=str(pack_meta.get("description", "")),
        path=pack_path,
        rules=rules,
    )


def validate_rule_pack(path: str | Path) -> list[str]:
    """Return validation errors for a pack. Empty list means valid."""

    try:
        load_rule_pack(path)
    except RulePackError as exc:
        return [str(exc)]
    return []


def _load_rule(raw_rule: Any, pack_id: str, pack_version: str, pack_path: Path) -> Rule:
    if not isinstance(raw_rule, dict):
        raise RulePackError(f"{pack_path}: each rule must be a mapping")

    rule_id = _require_str(raw_rule, "id", pack_path)
    rule_type = _require_str(raw_rule, "type", pack_path).lower()
    severity = _require_str(raw_rule, "severity", pack_path).upper()
    if severity not in SEVERITY_ORDER:
        raise RulePackError(f"{pack_path}: {rule_id} has invalid severity {severity!r}")

    languages = raw_rule.get("languages", [])
    if not isinstance(languages, list) or not all(isinstance(item, str) for item in languages):
        raise RulePackError(f"{pack_path}: {rule_id} languages must be a string list")

    patterns = ()
    if rule_type == "pattern":
        patterns = tuple(_load_patterns(raw_rule, rule_id, pack_path))
    elif rule_type == "ast":
        _validate_ast_rule(raw_rule, rule_id, pack_path)
    elif rule_type == "llm":
        _validate_llm_rule(raw_rule, rule_id, pack_path)
    elif rule_type not in RULE_TYPES:
        raise RulePackError(f"{pack_path}: {rule_id} has unknown type {rule_type!r}")

    references = tuple(_load_references(raw_rule.get("references", []), rule_id, pack_path))
    unknown_languages = sorted(set(languages) - SUPPORTED_LANGUAGES)
    if unknown_languages:
        raise RulePackError(
            f"{pack_path}: {rule_id} has unsupported language(s): {', '.join(unknown_languages)}"
        )

    return Rule(
        id=rule_id,
        name=_require_str(raw_rule, "name", pack_path),
        description=_require_str(raw_rule, "description", pack_path),
        type=rule_type,
        severity=severity,
        languages=tuple(languages),
        patterns=patterns,
        message=_require_str(raw_rule, "message", pack_path),
        fix_hint=_require_str(raw_rule, "fix_hint", pack_path),
        references=references,
        tags=_string_tuple(raw_rule.get("tags", []), "tags", rule_id, pack_path),
        enabled=bool(raw_rule.get("enabled", True)),
        pack_id=pack_id,
        pack_version=pack_version,
        raw=raw_rule,
    )


def _load_patterns(raw_rule: dict[str, Any], rule_id: str, pack_path: Path) -> list[RulePattern]:
    raw_patterns = raw_rule.get("patterns")
    if not isinstance(raw_patterns, list) or not raw_patterns:
        raise RulePackError(f"{pack_path}: {rule_id} pattern rule needs non-empty patterns")

    patterns: list[RulePattern] = []
    for item in raw_patterns:
        if isinstance(item, str):
            regex = item
            description = ""
            exclude_patterns: tuple[str, ...] = ()
        elif isinstance(item, dict):
            regex = _require_str(item, "regex", pack_path)
            description = str(item.get("description", ""))
            raw_excludes = item.get("exclude_patterns", [])
            if not isinstance(raw_excludes, list):
                raise RulePackError(f"{pack_path}: {rule_id} exclude_patterns must be a list")
            exclude_patterns = tuple(str(value) for value in raw_excludes)
        else:
            raise RulePackError(f"{pack_path}: {rule_id} pattern entries must be strings or mappings")

        _compile_regex(regex, pack_path, rule_id)
        for exclude in exclude_patterns:
            _compile_regex(exclude, pack_path, rule_id)
        patterns.append(RulePattern(regex=regex, description=description, exclude_patterns=exclude_patterns))

    return patterns


def _load_references(raw_refs: Any, rule_id: str, pack_path: Path) -> list[dict[str, str]]:
    if raw_refs is None:
        return []
    if not isinstance(raw_refs, list):
        raise RulePackError(f"{pack_path}: {rule_id} references must be a list")
    refs: list[dict[str, str]] = []
    for ref in raw_refs:
        if not isinstance(ref, dict):
            raise RulePackError(f"{pack_path}: {rule_id} reference entries must be mappings")
        if "url" not in ref or "title" not in ref:
            raise RulePackError(f"{pack_path}: {rule_id} references need url and title")
        refs.append({str(key): str(value) for key, value in ref.items()})
    return refs


def _validate_ast_rule(raw_rule: dict[str, Any], rule_id: str, pack_path: Path) -> None:
    raw_ast = raw_rule.get("ast")
    if not isinstance(raw_ast, dict):
        raise RulePackError(f"{pack_path}: {rule_id} ast rule needs an ast mapping")

    node_type = _require_str(raw_ast, "node_type", pack_path)
    if node_type != "function":
        raise RulePackError(f"{pack_path}: {rule_id} ast.node_type must be 'function'")

    name_matches = _require_str(raw_ast, "name_matches", pack_path)
    _compile_regex(name_matches, pack_path, rule_id)

    must_contain = raw_ast.get("must_contain", [])
    if not isinstance(must_contain, list) or not all(isinstance(item, str) for item in must_contain):
        raise RulePackError(f"{pack_path}: {rule_id} ast.must_contain must be a string list")
    if not must_contain:
        raise RulePackError(f"{pack_path}: {rule_id} ast.must_contain must not be empty")
    for pattern in must_contain:
        _compile_regex(pattern, pack_path, rule_id)

    if raw_ast.get("if_missing") != "flag":
        raise RulePackError(f"{pack_path}: {rule_id} ast.if_missing must be 'flag'")


def _validate_llm_rule(raw_rule: dict[str, Any], rule_id: str, pack_path: Path) -> None:
    raw_llm = raw_rule.get("llm")
    if not isinstance(raw_llm, dict):
        raise RulePackError(f"{pack_path}: {rule_id} llm rule needs an llm mapping")

    scope = _require_str(raw_llm, "scope", pack_path)
    if scope not in {"file", "function"}:
        raise RulePackError(f"{pack_path}: {rule_id} llm.scope must be 'file' or 'function'")

    _require_str(raw_llm, "prompt", pack_path)


def _compile_regex(regex: str, pack_path: Path, rule_id: str) -> None:
    try:
        re.compile(regex)
    except re.error as exc:
        raise RulePackError(f"{pack_path}: {rule_id} invalid regex {regex!r}: {exc}") from exc


def _require_mapping(raw: dict[str, Any], key: str, pack_path: Path) -> dict[str, Any]:
    value = raw.get(key)
    if not isinstance(value, dict):
        raise RulePackError(f"{pack_path}: missing mapping {key!r}")
    return value


def _require_str(raw: dict[str, Any], key: str, pack_path: Path) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RulePackError(f"{pack_path}: missing string field {key!r}")
    return value


def _string_tuple(raw: Any, field: str, rule_id: str, pack_path: Path) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise RulePackError(f"{pack_path}: {rule_id} {field} must be a string list")
    return tuple(raw)
