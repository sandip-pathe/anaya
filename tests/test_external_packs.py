from pathlib import Path

from anaya.engine.orchestrator import ScanOrchestrator
from anaya.engine.rule_loader import load_rule_pack


def test_external_policy_pack_can_be_loaded_and_scanned(tmp_path: Path):
    pack_path = tmp_path / "custom-policy.yml"
    source_path = tmp_path / "service.py"

    pack_path.write_text(
        "\n".join(
            [
                "pack:",
                '  id: "custom/internal-policy"',
                '  version: "1.0.0"',
                '  name: "Internal Policy"',
                '  description: "User-authored policy pack"',
                "rules:",
                '  - id: "CUSTOM-001"',
                '    name: "No Debug Payment Bypass"',
                '    description: "Debug payment bypass must not be enabled."',
                "    type: pattern",
                "    severity: HIGH",
                "    languages: [python]",
                "    patterns:",
                "      - regex: 'debug_payment_bypass\\s*=\\s*True'",
                '        description: "Matches enabled bypass flags."',
                '    message: "Debug payment bypass enabled at line {line}."',
                '    fix_hint: "Remove the bypass flag."',
                "    tags: [custom]",
                "    enabled: true",
                "",
            ]
        ),
        encoding="utf-8",
    )
    source_path.write_text("debug_payment_bypass = True\n", encoding="utf-8")

    pack = load_rule_pack(pack_path)
    summary = ScanOrchestrator([pack]).scan_paths([source_path])

    assert pack.id == "custom/internal-policy"
    assert summary.total_violations == 1
    assert summary.results[0].violations[0].rule_id == "CUSTOM-001"
