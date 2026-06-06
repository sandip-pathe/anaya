"""Deterministic regex-based scanner."""

from __future__ import annotations

from pathlib import Path
import re

from anaya.engine.models import Rule, Violation
from anaya.engine.scanners.base import Scanner


LANGUAGE_BY_SUFFIX = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rb": "ruby",
    ".rs": "rust",
}


class PatternScanner(Scanner):
    """Scan source text with rule-pack regex patterns."""

    def scan_file_content(
        self,
        file_path: str,
        content: str,
        rules: list[Rule],
    ) -> list[Violation]:
        language = detect_language(file_path)
        if language is None:
            return []

        violations: list[Violation] = []
        seen: set[tuple[str, int, str]] = set()

        for rule in rules:
            if not _rule_applies(rule, language):
                continue
            for line_number, line in enumerate(content.splitlines(), start=1):
                if _has_inline_suppression(line, rule.id):
                    continue
                for pattern in rule.patterns:
                    if any(re.search(exclude, line, re.IGNORECASE) for exclude in pattern.exclude_patterns):
                        continue
                    match = re.search(pattern.regex, line, re.IGNORECASE)
                    if not match:
                        continue
                    key = (rule.id, line_number, line.strip())
                    if key in seen:
                        continue
                    seen.add(key)
                    violations.append(_build_violation(rule, file_path, line_number, line, match))

        return sorted(violations, key=lambda item: (item.line_number, item.rule_id))


def detect_language(file_path: str) -> str | None:
    """Detect a source language from file extension."""

    return LANGUAGE_BY_SUFFIX.get(Path(file_path).suffix.lower())


def supported_source_file(path: Path) -> bool:
    """Return true when a file extension can be scanned."""

    return path.is_file() and detect_language(str(path)) is not None


def _rule_applies(rule: Rule, language: str) -> bool:
    return (
        rule.enabled
        and rule.type == "pattern"
        and bool(rule.patterns)
        and (not rule.languages or language in rule.languages)
    )


def _has_inline_suppression(line: str, rule_id: str) -> bool:
    lowered = line.lower()
    return (
        f"noqa: {rule_id.lower()}" in lowered
        or f"noqa:{rule_id.lower()}" in lowered
        or "noqa: anaya" in lowered
        or "noqa:anaya" in lowered
    )


def _build_violation(
    rule: Rule,
    file_path: str,
    line_number: int,
    line: str,
    match: re.Match[str],
) -> Violation:
    snippet = line.rstrip()
    message = _render_template(
        rule.message,
        {
            "line": line_number,
            "file": file_path,
            "match": match.group(0),
            "rule": rule.id,
        },
    )
    return Violation(
        rule_id=rule.id,
        rule_name=rule.name,
        severity=rule.severity,
        file_path=file_path,
        line_number=line_number,
        end_line=None,
        column=match.start() + 1,
        snippet=snippet,
        message=message,
        fix_hint=rule.fix_hint,
        references=rule.references,
        pack_id=rule.pack_id,
        confidence=1.0,
    )


def _render_template(template: str, values: dict[str, object]) -> str:
    try:
        return template.format(**values)
    except (KeyError, ValueError):
        return template
