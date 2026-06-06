"""GitHub Check Run payload formatting."""

from __future__ import annotations

from pathlib import Path

from anaya.engine.models import ScanSummary, Violation


MAX_GITHUB_ANNOTATIONS = 50

SEVERITY_TO_ANNOTATION_LEVEL = {
    "CRITICAL": "failure",
    "HIGH": "failure",
    "MEDIUM": "warning",
    "LOW": "notice",
    "INFO": "notice",
}


def build_check_run_payloads(
    summary: ScanSummary,
    *,
    title: str = "Anaya Policy Scan",
    annotation_limit: int = MAX_GITHUB_ANNOTATIONS,
) -> list[dict[str, object]]:
    """Build one or more GitHub Check Run update payloads."""

    violations = [violation for result in summary.results for violation in result.violations]
    batches = _batches(violations, annotation_limit)
    if not batches:
        batches = [[]]

    payloads: list[dict[str, object]] = []
    for index, batch in enumerate(batches):
        payload = {
            "status": "completed",
            "conclusion": _conclusion(summary.overall_status),
            "output": {
                "title": title if len(batches) == 1 else f"{title} ({index + 1}/{len(batches)})",
                "summary": _summary_markdown(summary, len(violations), index, len(batches)),
                "annotations": [_annotation(violation) for violation in batch],
            },
        }
        payloads.append(payload)
    return payloads


def _batches(violations: list[Violation], annotation_limit: int) -> list[list[Violation]]:
    if annotation_limit <= 0:
        raise ValueError("annotation_limit must be greater than zero")
    return [
        violations[index : index + annotation_limit]
        for index in range(0, len(violations), annotation_limit)
    ]


def _conclusion(status: str) -> str:
    if status == "FAIL":
        return "failure"
    if status == "WARN":
        return "neutral"
    return "success"


def _summary_markdown(
    summary: ScanSummary,
    total_annotations: int,
    batch_index: int,
    batch_count: int,
) -> str:
    lines = [
        f"**Status:** {summary.overall_status}",
        f"**Files scanned:** {summary.total_files}",
        f"**Violations:** {summary.total_violations}",
        f"**Rules checked:** {summary.rules_checked}",
    ]
    if summary.by_severity:
        severity = ", ".join(
            f"{name}: {count}" for name, count in summary.by_severity.items() if count
        )
        if severity:
            lines.append(f"**Severity:** {severity}")
    if batch_count > 1:
        lines.append(
            f"Showing annotations {batch_index + 1} of {batch_count}; "
            f"{total_annotations} total annotations were produced."
        )
    if summary.warnings:
        lines.append("**Warnings:** " + "; ".join(summary.warnings))
    return "\n\n".join(lines)


def _annotation(violation: Violation) -> dict[str, object]:
    return {
        "path": Path(violation.file_path).as_posix(),
        "start_line": violation.line_number,
        "end_line": violation.end_line or violation.line_number,
        "annotation_level": SEVERITY_TO_ANNOTATION_LEVEL.get(violation.severity, "warning"),
        "title": f"{violation.rule_id}: {violation.rule_name}",
        "message": f"{violation.message}\n\nFix: {violation.fix_hint}",
        "raw_details": violation.snippet,
    }
