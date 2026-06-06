"""JSON reporting."""

from __future__ import annotations

from dataclasses import asdict
import json

from anaya.engine.models import ScanSummary


def format_json(summary: ScanSummary) -> str:
    """Serialize a scan summary to pretty JSON."""

    return json.dumps(asdict(summary), indent=2, ensure_ascii=False)
