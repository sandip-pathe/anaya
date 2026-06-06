"""Core scan orchestration."""

from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path
from time import perf_counter

from anaya.engine.models import Rule, RulePack, ScanResult, ScanSummary, Violation, severity_at_least
from anaya.engine.rule_loader import load_rule_pack
from anaya.engine.scanners.ast_scanner import AstScanner
from anaya.engine.scanners.pattern import PatternScanner, detect_language, supported_source_file


DEFAULT_IGNORES = (
    ".git/**",
    ".venv/**",
    "venv/**",
    "env/**",
    "node_modules/**",
    "dist/**",
    "build/**",
    "*.generated.*",
)
MAX_FILE_SIZE_BYTES = 1_000_000


class ScanOrchestrator:
    """Coordinate rule packs and scanners over one or more paths."""

    def __init__(self, packs: list[RulePack]):
        self.packs = packs
        self.rules = [rule for pack in packs for rule in pack.rules if rule.enabled]
        self.pattern_scanner = PatternScanner()
        self.ast_scanner = AstScanner()

    @classmethod
    def from_pack_paths(cls, pack_paths: list[str | Path]) -> "ScanOrchestrator":
        return cls([load_rule_pack(path) for path in pack_paths])

    def scan_paths(
        self,
        paths: list[str | Path],
        *,
        fail_on: str = "CRITICAL",
        warn_on: str = "HIGH",
        ignore: tuple[str, ...] = DEFAULT_IGNORES,
        ignored_rules: tuple[str, ...] = (),
        languages: tuple[str, ...] = (),
        config_path: str | None = None,
    ) -> ScanSummary:
        started = perf_counter()
        files, skipped_files = collect_files(paths, ignore, languages=languages)
        ignored_rule_ids = set(ignored_rules)
        selected_languages = set(languages)
        active_rules = self._active_rules(ignored_rule_ids, selected_languages)

        results: list[ScanResult] = []
        for file_path in files:
            file_started = perf_counter()
            content = file_path.read_text(encoding="utf-8", errors="replace")
            results.append(self._scan_one(str(file_path), content, active_rules, file_started))

        scan_duration_ms = (perf_counter() - started) * 1000
        return self._summarize_results(
            results,
            fail_on,
            warn_on,
            scan_duration_ms,
            rules_checked=len(active_rules),
            skipped_files=skipped_files,
            config_path=config_path,
        )

    def scan_contents(
        self,
        files: list[tuple[str, str]],
        *,
        fail_on: str = "CRITICAL",
        warn_on: str = "HIGH",
        ignored_rules: tuple[str, ...] = (),
        languages: tuple[str, ...] = (),
        config_path: str | None = None,
    ) -> ScanSummary:
        """Scan in-memory source files using repo-relative paths."""

        started = perf_counter()
        ignored_rule_ids = set(ignored_rules)
        selected_languages = set(languages)
        active_rules = self._active_rules(ignored_rule_ids, selected_languages)
        skipped_files = {"unsupported": 0, "language_filtered": 0}

        results: list[ScanResult] = []
        for file_path, content in files:
            language = detect_language(file_path)
            if language is None:
                skipped_files["unsupported"] += 1
                continue
            if selected_languages and language not in selected_languages:
                skipped_files["language_filtered"] += 1
                continue
            file_started = perf_counter()
            results.append(self._scan_one(file_path, content, active_rules, file_started))

        scan_duration_ms = (perf_counter() - started) * 1000
        return self._summarize_results(
            results,
            fail_on,
            warn_on,
            scan_duration_ms,
            rules_checked=len(active_rules),
            skipped_files={key: value for key, value in skipped_files.items() if value},
            config_path=config_path,
        )

    def _active_rules(self, ignored_rule_ids: set[str], selected_languages: set[str]) -> list[Rule]:
        return [
            rule
            for rule in self.rules
            if rule.id not in ignored_rule_ids and _rule_matches_selected_languages(rule, selected_languages)
        ]

    def _scan_one(
        self,
        file_path: str,
        content: str,
        active_rules: list[Rule],
        file_started: float,
    ) -> ScanResult:
        violations = [
            *self.pattern_scanner.scan_file_content(file_path, content, active_rules),
            *self.ast_scanner.scan_file_content(file_path, content, active_rules),
        ]
        elapsed_ms = (perf_counter() - file_started) * 1000
        return ScanResult(
            file_path=file_path,
            violations=tuple(violations),
            rules_checked=len(active_rules),
            scan_duration_ms=elapsed_ms,
        )

    def _summarize_results(
        self,
        results: list[ScanResult],
        fail_on: str,
        warn_on: str,
        scan_duration_ms: float,
        *,
        rules_checked: int,
        skipped_files: dict[str, int],
        config_path: str | None,
    ) -> ScanSummary:
        all_violations = [violation for result in results for violation in result.violations]
        return _summarize(
            results,
            all_violations,
            fail_on,
            warn_on,
            scan_duration_ms,
            rules_checked=rules_checked,
            skipped_files=skipped_files,
            pack_versions={pack.id: pack.version for pack in self.packs},
            config_path=config_path,
        )


def built_in_pack_paths() -> list[Path]:
    """Return all bundled rule pack YAML paths."""

    packs_dir = Path(__file__).resolve().parents[1] / "packs"
    return sorted(packs_dir.glob("**/*.yml"))


def resolve_pack_identifier(identifier: str | Path, *, base_dir: str | Path | None = None) -> Path:
    """Resolve a file path or built-in pack id like generic/secrets-detection."""

    candidate = Path(identifier)
    if base_dir is not None and not candidate.is_absolute():
        scoped_candidate = Path(base_dir) / candidate
        if scoped_candidate.exists():
            return scoped_candidate
    if candidate.exists():
        return candidate
    packs_dir = Path(__file__).resolve().parents[1] / "packs"
    built_in = packs_dir.joinpath(*str(identifier).split("/")).with_suffix(".yml")
    if built_in.exists():
        return built_in
    raise FileNotFoundError(f"Unknown pack: {identifier}")


def collect_files(
    paths: list[str | Path],
    ignore: tuple[str, ...],
    *,
    languages: tuple[str, ...] = (),
) -> tuple[list[Path], dict[str, int]]:
    files: list[Path] = []
    skipped = {
        "ignored": 0,
        "unsupported": 0,
        "language_filtered": 0,
        "binary": 0,
        "too_large": 0,
        "missing": 0,
    }
    selected_languages = set(languages)
    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            skipped["missing"] += 1
            continue
        if path.is_file():
            _append_file(path, ignore, files, skipped, selected_languages)
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file():
                    _append_file(child, ignore, files, skipped, selected_languages)
    return sorted(dict.fromkeys(files)), {key: value for key, value in skipped.items() if value}


def _append_file(
    path: Path,
    ignore: tuple[str, ...],
    files: list[Path],
    skipped: dict[str, int],
    selected_languages: set[str],
) -> None:
    if _ignored(path, ignore):
        skipped["ignored"] += 1
        return
    if not supported_source_file(path):
        skipped["unsupported"] += 1
        return
    language = detect_language(str(path))
    if selected_languages and language not in selected_languages:
        skipped["language_filtered"] += 1
        return
    try:
        if path.stat().st_size > MAX_FILE_SIZE_BYTES:
            skipped["too_large"] += 1
            return
        if _looks_binary(path):
            skipped["binary"] += 1
            return
    except OSError:
        skipped["missing"] += 1
        return
    files.append(path)


def _ignored(path: Path, ignore: tuple[str, ...]) -> bool:
    normalized = path.as_posix()
    parts = set(path.parts)
    return any(
        fnmatch(normalized, pattern)
        or fnmatch(path.name, pattern)
        or pattern.rstrip("/**") in parts
        for pattern in ignore
    )


def _looks_binary(path: Path) -> bool:
    sample = path.read_bytes()[:2048]
    return b"\x00" in sample


def _rule_matches_selected_languages(rule: Rule, selected_languages: set[str]) -> bool:
    return (
        not selected_languages
        or not rule.languages
        or bool(set(rule.languages) & selected_languages)
    )


def _summarize(
    results: list[ScanResult],
    violations: list[Violation],
    fail_on: str,
    warn_on: str,
    scan_duration_ms: float,
    *,
    rules_checked: int,
    skipped_files: dict[str, int],
    pack_versions: dict[str, str],
    config_path: str | None,
) -> ScanSummary:
    by_severity = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    by_pack: dict[str, dict[str, int | str]] = {}

    status = "PASS"
    for violation in violations:
        by_severity[violation.severity] = by_severity.get(violation.severity, 0) + 1
        pack_stats = by_pack.setdefault(
            violation.pack_id,
            {"status": "PASS", "total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0},
        )
        pack_stats["total"] = int(pack_stats["total"]) + 1
        pack_stats[violation.severity.lower()] = int(pack_stats.get(violation.severity.lower(), 0)) + 1
        if severity_at_least(violation.severity, fail_on):
            status = "FAIL"
            pack_stats["status"] = "FAIL"
        elif severity_at_least(violation.severity, warn_on):
            if status != "FAIL":
                status = "WARN"
            if pack_stats["status"] != "FAIL":
                pack_stats["status"] = "WARN"

    return ScanSummary(
        total_files=len(results),
        total_violations=len(violations),
        by_severity=by_severity,
        by_pack=by_pack,
        overall_status=status,
        scan_duration_ms=scan_duration_ms,
        results=tuple(results),
        rules_checked=rules_checked,
        skipped_files=skipped_files,
        pack_versions=pack_versions,
        config_path=config_path,
    )
