"""Markdown summary for optional pull request comments."""

from __future__ import annotations

from anaya.engine.models import ScanSummary


def format_pr_comment(summary: ScanSummary) -> str:
    """Return a concise Markdown scan summary for PR comments."""

    lines = [
        "## Anaya Policy Scan",
        "",
        f"**Status:** {summary.overall_status}",
        f"**Files scanned:** {summary.total_files}",
        f"**Violations:** {summary.total_violations}",
        f"**Rules checked:** {summary.rules_checked}",
        "",
        "| Pack | Status | Findings |",
        "| --- | --- | ---: |",
    ]
    if summary.by_pack:
        for pack_id, stats in sorted(summary.by_pack.items()):
            lines.append(f"| `{pack_id}` | {stats['status']} | {stats['total']} |")
    else:
        lines.append("| None | PASS | 0 |")

    violations = [violation for result in summary.results for violation in result.violations]
    if violations:
        lines.extend(["", "### Top Findings", ""])
        for violation in violations[:10]:
            lines.append(
                f"- **{violation.severity}** `{violation.rule_id}` "
                f"{violation.file_path}:{violation.line_number} - {violation.rule_name}"
            )
        if len(violations) > 10:
            lines.append(f"- {len(violations) - 10} more finding(s) omitted from comment summary.")
    else:
        lines.extend(["", "No findings."])

    if summary.warnings:
        lines.extend(["", "### Warnings", ""])
        lines.extend(f"- {warning}" for warning in summary.warnings)

    return "\n".join(lines)
