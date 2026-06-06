"""Repository-level anaya.yml loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from anaya.engine.models import SEVERITY_ORDER, SUPPORTED_LANGUAGES
from anaya.engine.orchestrator import resolve_pack_identifier
from anaya.engine.rule_loader import RulePackError, load_rule_pack


DEFAULT_PACKS = (
    "generic/secrets-detection",
    "generic/owasp-top10",
    "generic/pii-handling",
    "generic/tls-encryption",
    "generic/audit-logging",
)


@dataclass(frozen=True)
class ThresholdConfig:
    fail_on: str = "CRITICAL"
    warn_on: str = "HIGH"


@dataclass(frozen=True)
class IgnoreConfig:
    paths: tuple[str, ...] = ()
    rules: tuple[str, ...] = ()


@dataclass(frozen=True)
class LlmConfig:
    enabled: bool = False


@dataclass(frozen=True)
class RepositoryConfig:
    version: str = "1"
    packs: tuple[str, ...] = DEFAULT_PACKS
    scan_mode: str = "diff"
    languages: tuple[str, ...] = ()
    thresholds: ThresholdConfig = ThresholdConfig()
    ignore: IgnoreConfig = IgnoreConfig()
    llm: LlmConfig = LlmConfig()


class RepositoryConfigError(ValueError):
    """Raised when an anaya.yml file is malformed."""


def find_config(start: str | Path) -> Path | None:
    """Find anaya.yml from a path or one of its parents."""

    path = Path(start).resolve()
    current = path if path.is_dir() else path.parent
    for candidate_dir in (current, *current.parents):
        candidate = candidate_dir / "anaya.yml"
        if candidate.exists():
            return candidate
    return None


def load_repository_config(path: str | Path | None) -> RepositoryConfig:
    """Load repository config, returning defaults when path is None."""

    if path is None:
        return RepositoryConfig()

    config_path = Path(path)
    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise RepositoryConfigError(f"Malformed YAML in {config_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise RepositoryConfigError(f"{config_path}: config must be a mapping")

    packs = _load_packs(raw.get("packs", DEFAULT_PACKS), config_path)
    scan_raw = _mapping(raw.get("scan", {}), "scan", config_path)
    thresholds_raw = _mapping(raw.get("thresholds", {}), "thresholds", config_path)
    ignore_raw = _mapping(raw.get("ignore", {}), "ignore", config_path)
    llm_raw = _mapping(raw.get("llm", {}), "llm", config_path)
    ignore_paths = _string_tuple(ignore_raw.get("paths", []), "ignore.paths", config_path)
    ignore_rules = _string_tuple(ignore_raw.get("rules", []), "ignore.rules", config_path)
    llm_enabled = _bool(llm_raw.get("enabled", False), "llm.enabled", config_path)

    scan_mode = str(scan_raw.get("mode", "diff"))
    if scan_mode not in {"diff", "full"}:
        raise RepositoryConfigError(f"{config_path}: scan.mode must be 'diff' or 'full'")

    fail_on = str(thresholds_raw.get("fail_on", "CRITICAL")).upper()
    warn_on = str(thresholds_raw.get("warn_on", "HIGH")).upper()
    _validate_severity(fail_on, "thresholds.fail_on", config_path)
    _validate_severity(warn_on, "thresholds.warn_on", config_path)

    languages = _string_tuple(scan_raw.get("languages", []), "scan.languages", config_path)
    unknown_languages = sorted(set(languages) - SUPPORTED_LANGUAGES)
    if unknown_languages:
        raise RepositoryConfigError(
            f"{config_path}: unsupported language(s): {', '.join(unknown_languages)}"
        )

    known_rule_ids: set[str] = set()
    for pack in packs:
        try:
            pack_path = resolve_pack_identifier(pack, base_dir=config_path.parent)
        except FileNotFoundError as exc:
            raise RepositoryConfigError(f"{config_path}: unknown pack {pack!r}") from exc
        try:
            known_rule_ids.update(rule.id for rule in load_rule_pack(pack_path).rules)
        except RulePackError as exc:
            raise RepositoryConfigError(f"{config_path}: invalid pack {pack!r}: {exc}") from exc

    unknown_ignored_rules = sorted(set(ignore_rules) - known_rule_ids)
    if unknown_ignored_rules:
        raise RepositoryConfigError(
            f"{config_path}: ignore.rules contains unknown rule(s): "
            f"{', '.join(unknown_ignored_rules)}"
        )

    return RepositoryConfig(
        version=str(raw.get("version", "1")),
        packs=packs,
        scan_mode=scan_mode,
        languages=languages,
        thresholds=ThresholdConfig(fail_on=fail_on, warn_on=warn_on),
        ignore=IgnoreConfig(paths=ignore_paths, rules=ignore_rules),
        llm=LlmConfig(enabled=llm_enabled),
    )


def _load_packs(raw_packs: Any, config_path: Path) -> tuple[str, ...]:
    if not isinstance(raw_packs, list) or not raw_packs:
        raise RepositoryConfigError(f"{config_path}: packs must be a non-empty list")

    packs: list[str] = []
    for item in raw_packs:
        if isinstance(item, str):
            packs.append(item)
        elif isinstance(item, dict) and isinstance(item.get("id"), str):
            packs.append(item["id"])
        else:
            raise RepositoryConfigError(f"{config_path}: each pack must be a string or mapping with id")
    return tuple(packs)


def _mapping(raw: Any, name: str, config_path: Path) -> dict[str, Any]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise RepositoryConfigError(f"{config_path}: {name} must be a mapping")
    return raw


def _string_tuple(raw: Any, name: str, config_path: Path) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise RepositoryConfigError(f"{config_path}: {name} must be a string list")
    return tuple(raw)


def _validate_severity(value: str, name: str, config_path: Path) -> None:
    if value not in SEVERITY_ORDER:
        raise RepositoryConfigError(f"{config_path}: {name} has invalid severity {value!r}")


def _bool(raw: Any, name: str, config_path: Path) -> bool:
    if isinstance(raw, bool):
        return raw
    raise RepositoryConfigError(f"{config_path}: {name} must be a boolean")
