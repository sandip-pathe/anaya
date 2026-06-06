"""Audit-oriented JSON reporting."""

from __future__ import annotations

from dataclasses import asdict
import json

from anaya.engine.models import ScanSummary


def format_audit_json(summary: ScanSummary) -> str:
    """Serialize scan output with audit metadata grouped for later exports."""

    payload = {
        "tool": {"name": "Anaya", "version": "0.1.0"},
        "scan": {
            "overall_status": summary.overall_status,
            "duration_ms": summary.scan_duration_ms,
            "config_path": summary.config_path,
            "pack_versions": summary.pack_versions,
            "rules_checked": summary.rules_checked,
            "skipped_files": summary.skipped_files,
            "warnings": summary.warnings,
        },
        "summary": {
            "total_files": summary.total_files,
            "total_violations": summary.total_violations,
            "by_severity": summary.by_severity,
            "by_pack": summary.by_pack,
        },
        "results": [asdict(result) for result in summary.results],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)
