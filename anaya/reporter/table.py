"""Human-readable terminal output."""

from __future__ import annotations

from anaya.engine.models import ScanSummary


def format_table(summary: ScanSummary) -> str:
    """Return a compact text table without requiring Rich at engine runtime."""

    lines = [
        f"Anaya Policy Scan - {summary.total_violations} violation(s)",
        f"Status: {summary.overall_status}",
        f"Files scanned: {summary.total_files}",
        f"Duration: {summary.scan_duration_ms:.1f} ms",
        "",
        "Severity: "
        + ", ".join(f"{name}={count}" for name, count in summary.by_severity.items() if count),
    ]

    if summary.by_pack:
        lines.extend(["", "Packs:"])
        for pack_id, stats in sorted(summary.by_pack.items()):
            lines.append(f"  {pack_id}: {stats['status']} ({stats['total']} finding(s))")

    violations = [violation for result in summary.results for violation in result.violations]
    if violations:
        lines.extend(["", "Findings:"])
    for violation in violations:
        lines.extend(
            [
                f"  {violation.severity} {violation.file_path}:{violation.line_number}",
                f"  {violation.rule_id}: {violation.rule_name}",
                f"  {violation.message}",
                f"  > {violation.snippet.strip()}",
                f"  Fix: {violation.fix_hint}",
                "",
            ]
        )

    return "\n".join(lines).rstrip()
