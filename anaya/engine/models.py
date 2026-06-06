"""Shared engine data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


SEVERITY_ORDER = {
    "INFO": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
}

SUPPORTED_LANGUAGES = {
    "python",
    "javascript",
    "typescript",
    "java",
    "go",
    "ruby",
    "rust",
}

RULE_TYPES = {"pattern", "ast", "llm"}


@dataclass(frozen=True)
class RulePattern:
    regex: str
    description: str = ""
    exclude_patterns: tuple[str, ...] = ()


@dataclass(frozen=True)
class Rule:
    id: str
    name: str
    description: str
    type: str
    severity: str
    languages: tuple[str, ...]
    message: str
    fix_hint: str
    references: tuple[dict[str, str], ...] = ()
    tags: tuple[str, ...] = ()
    enabled: bool = True
    pack_id: str = ""
    pack_version: str = ""
    patterns: tuple[RulePattern, ...] = ()
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RulePack:
    id: str
    version: str
    name: str
    description: str
    path: Path
    rules: tuple[Rule, ...]


@dataclass(frozen=True)
class Violation:
    rule_id: str
    rule_name: str
    severity: str
    file_path: str
    line_number: int
    end_line: int | None
    column: int | None
    snippet: str
    message: str
    fix_hint: str
    references: tuple[dict[str, str], ...]
    pack_id: str
    confidence: float


@dataclass(frozen=True)
class ScanResult:
    file_path: str
    violations: tuple[Violation, ...]
    rules_checked: int
    scan_duration_ms: float


@dataclass(frozen=True)
class ScanSummary:
    total_files: int
    total_violations: int
    by_severity: dict[str, int]
    by_pack: dict[str, dict[str, int | str]]
    overall_status: str
    scan_duration_ms: float
    results: tuple[ScanResult, ...]
    rules_checked: int = 0
    skipped_files: dict[str, int] = field(default_factory=dict)
    config_path: str | None = None
    pack_versions: dict[str, str] = field(default_factory=dict)


def severity_at_least(value: str, threshold: str) -> bool:
    """Return true when value is equal to or higher than threshold."""

    return SEVERITY_ORDER.get(value.upper(), -1) >= SEVERITY_ORDER.get(threshold.upper(), 999)
