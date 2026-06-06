"""Core scan orchestration."""

from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path
from time import perf_counter

from anaya.engine.models import RulePack, ScanResult, ScanSummary, Violation, severity_at_least
from anaya.engine.rule_loader import load_rule_pack
from anaya.engine.scanners.pattern import PatternScanner, supported_source_file


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


class ScanOrchestrator:
    """Coordinate rule packs and scanners over one or more paths."""

    def __init__(self, packs: list[RulePack]):
        self.packs = packs
        self.rules = [rule for pack in packs for rule in pack.rules if rule.enabled]
        self.pattern_scanner = PatternScanner()

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
    ) -> ScanSummary:
        started = perf_counter()
        files = _collect_files(paths, ignore)
        ignored_rule_ids = set(ignored_rules)
        active_rules = [rule for rule in self.rules if rule.id not in ignored_rule_ids]

        results: list[ScanResult] = []
        for file_path in files:
            file_started = perf_counter()
            content = file_path.read_text(encoding="utf-8", errors="replace")
            violations = self.pattern_scanner.scan_file_content(
                str(file_path),
                content,
                active_rules,
            )
            elapsed_ms = (perf_counter() - file_started) * 1000
            results.append(
                ScanResult(
                    file_path=str(file_path),
                    violations=tuple(violations),
                    rules_checked=len(active_rules),
                    scan_duration_ms=elapsed_ms,
                )
            )

        scan_duration_ms = (perf_counter() - started) * 1000
        all_violations = [violation for result in results for violation in result.violations]
        return _summarize(results, all_violations, fail_on, warn_on, scan_duration_ms)


def built_in_pack_paths() -> list[Path]:
    """Return all bundled rule pack YAML paths."""

    packs_dir = Path(__file__).resolve().parents[1] / "packs"
    return sorted(packs_dir.glob("**/*.yml"))


def resolve_pack_identifier(identifier: str | Path) -> Path:
    """Resolve a file path or built-in pack id like generic/secrets-detection."""

    candidate = Path(identifier)
    if candidate.exists():
        return candidate
    packs_dir = Path(__file__).resolve().parents[1] / "packs"
    built_in = packs_dir.joinpath(*str(identifier).split("/")).with_suffix(".yml")
    if built_in.exists():
        return built_in
    raise FileNotFoundError(f"Unknown pack: {identifier}")


def _collect_files(paths: list[str | Path], ignore: tuple[str, ...]) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_file() and supported_source_file(path) and not _ignored(path, ignore):
            files.append(path)
        elif path.is_dir():
            for child in path.rglob("*"):
                if supported_source_file(child) and not _ignored(child, ignore):
                    files.append(child)
    return sorted(dict.fromkeys(files))


def _ignored(path: Path, ignore: tuple[str, ...]) -> bool:
    normalized = path.as_posix()
    return any(fnmatch(normalized, pattern) for pattern in ignore)


def _summarize(
    results: list[ScanResult],
    violations: list[Violation],
    fail_on: str,
    warn_on: str,
    scan_duration_ms: float,
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
        elif status != "FAIL" and severity_at_least(violation.severity, warn_on):
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
    )
