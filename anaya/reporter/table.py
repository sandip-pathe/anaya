"""Human-readable terminal output."""

from __future__ import annotations

from anaya.engine.models import ScanSummary


def format_table(summary: ScanSummary) -> str:
    """Return a compact text table without requiring Rich at engine runtime."""

    lines = [
        f"Anaya Policy Scan - {summary.total_violations} violation(s)",
        f"Status: {summary.overall_status}",
        f"Files scanned: {summary.total_files}",
        f"Rules checked: {summary.rules_checked}",
        f"Duration: {summary.scan_duration_ms:.1f} ms",
    ]
    if summary.config_path:
        lines.append(f"Config: {summary.config_path}")
    if summary.skipped_files:
        lines.append("Skipped: " + ", ".join(f"{key}={value}" for key, value in summary.skipped_files.items()))
    if summary.warnings:
        lines.append("Warnings: " + "; ".join(summary.warnings))
    if summary.pack_versions:
        lines.append(
            "Pack versions: "
            + ", ".join(
                f"{pack_id}@{version}" for pack_id, version in sorted(summary.pack_versions.items())
            )
        )
    severity = ", ".join(f"{name}={count}" for name, count in summary.by_severity.items() if count)
    lines.extend(["", f"Severity: {severity or 'none'}"])

    if summary.by_pack:
        lines.extend(["", "Packs:"])
        for pack_id, stats in sorted(summary.by_pack.items()):
            lines.append(f"  {pack_id}: {stats['status']} ({stats['total']} finding(s))")

    violations = [violation for result in summary.results for violation in result.violations]
    lines.extend(["", "Findings:"])
    if not violations:
        lines.append("  No findings.")
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
