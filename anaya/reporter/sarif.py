"""Minimal SARIF 2.1.0 output."""

from __future__ import annotations

import json
from pathlib import Path

from anaya.engine.models import ScanSummary


SEVERITY_TO_SARIF_LEVEL = {
    "CRITICAL": "error",
    "HIGH": "error",
    "MEDIUM": "warning",
    "LOW": "note",
    "INFO": "note",
}


def format_sarif(summary: ScanSummary, *, automation_id: str = "anaya/default") -> str:
    """Format results as SARIF 2.1.0 JSON."""

    rules_by_id = {}
    results = []
    for scan_result in summary.results:
        for violation in scan_result.violations:
            first_reference = violation.references[0] if violation.references else {}
            rule_metadata = {
                "id": violation.rule_id,
                "name": violation.rule_name,
                "shortDescription": {"text": violation.rule_name},
                "fullDescription": {"text": violation.message},
                "defaultConfiguration": {
                    "level": SEVERITY_TO_SARIF_LEVEL.get(violation.severity, "warning")
                },
                "help": {"text": violation.fix_hint},
            }
            if first_reference.get("url"):
                rule_metadata["helpUri"] = first_reference["url"]
            rules_by_id.setdefault(
                violation.rule_id,
                rule_metadata,
            )
            results.append(
                {
                    "ruleId": violation.rule_id,
                    "level": SEVERITY_TO_SARIF_LEVEL.get(violation.severity, "warning"),
                    "message": {"text": violation.message},
                    "partialFingerprints": {
                        "anaya/v1": "|".join(
                            [
                                violation.rule_id,
                                Path(violation.file_path).as_posix(),
                                str(violation.line_number),
                                violation.snippet.strip(),
                            ]
                        )
                    },
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": Path(violation.file_path).as_posix()},
                                "region": {
                                    "startLine": violation.line_number,
                                    "startColumn": violation.column or 1,
                                },
                            }
                        }
                    ],
                }
            )

    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "automationDetails": {"id": automation_id},
                "tool": {
                    "driver": {
                        "name": "Anaya",
                        "version": "0.1.0",
                        "informationUri": "https://github.com/anaya-engine/anaya",
                        "rules": list(rules_by_id.values()),
                    }
                },
                "invocations": [{"executionSuccessful": True}],
                "columnKind": "utf16CodeUnits",
                "results": results,
            }
        ],
    }
    return json.dumps(sarif, indent=2, ensure_ascii=False)
