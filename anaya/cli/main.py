"""Anaya CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from anaya.engine.git_utils import GitDiffError, changed_files_since
from anaya.engine.orchestrator import (
    DEFAULT_IGNORES,
    ScanOrchestrator,
    built_in_pack_paths,
    resolve_pack_identifier,
)
from anaya.engine.repo_config import (
    DEFAULT_PACKS,
    RepositoryConfig,
    RepositoryConfigError,
    find_config,
    load_repository_config,
)
from anaya.engine.rule_loader import RulePackError, load_rule_pack, validate_rule_pack
from anaya.reporter.json_report import format_json
from anaya.reporter.sarif import format_sarif
from anaya.reporter.table import format_table

app = typer.Typer(help="Policy-as-code compliance scanner.")
packs_app = typer.Typer(help="Inspect bundled rule packs.")
app.add_typer(packs_app, name="packs")


@app.command()
def scan(
    path: Path = typer.Argument(Path("."), help="File or directory to scan."),
    pack: Optional[list[str]] = typer.Option(
        None,
        "--pack",
        "-p",
        help="Rule pack path or built-in id, e.g. generic/secrets-detection.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to anaya.yml. Auto-discovered when omitted.",
    ),
    no_config: bool = typer.Option(False, "--no-config", help="Ignore anaya.yml discovery."),
    output_format: str = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format: table, json, or sarif.",
    ),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Write output to a file."),
    diff: Optional[str] = typer.Option(None, "--diff", help="Scan files changed since REF."),
    fail_on: Optional[str] = typer.Option(None, "--fail-on", help="Minimum severity that fails."),
    warn_on: Optional[str] = typer.Option(None, "--warn-on", help="Minimum severity that warns."),
    no_color: bool = typer.Option(False, "--no-color", help="Disable color output."),
) -> None:
    """Scan a path with deterministic rule packs."""

    config_path, repo_config, orchestrator = _load_scan_context(path, pack, config, no_config)
    scan_paths = [path]
    if diff:
        diff_cwd = path if path.is_dir() else path.parent
        try:
            changed_paths = changed_files_since(diff, cwd=diff_cwd)
        except GitDiffError as exc:
            raise typer.BadParameter(str(exc)) from exc
        scan_paths = [
            changed_path if changed_path.is_absolute() else diff_cwd / changed_path
            for changed_path in changed_paths
        ]
    summary = orchestrator.scan_paths(
        scan_paths,
        fail_on=(fail_on or repo_config.thresholds.fail_on),
        warn_on=(warn_on or repo_config.thresholds.warn_on),
        ignore=DEFAULT_IGNORES + repo_config.ignore.paths,
        ignored_rules=repo_config.ignore.rules,
        languages=repo_config.languages,
        config_path=str(config_path) if config_path else None,
    )

    rendered = _render(summary, output_format)
    _write_or_echo(rendered, output)

    raise typer.Exit(code=1 if summary.overall_status == "FAIL" else 0)


@app.command("test-rule")
def test_rule(
    rule_id: str = typer.Option(..., "--rule", help="Rule ID to run in isolation."),
    file: Path = typer.Option(..., "--file", help="Source file to scan with the selected rule."),
    pack: Optional[list[str]] = typer.Option(
        None,
        "--pack",
        "-p",
        help="Rule pack path or built-in id, e.g. generic/secrets-detection.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to anaya.yml. Auto-discovered when omitted.",
    ),
    no_config: bool = typer.Option(False, "--no-config", help="Ignore anaya.yml discovery."),
    output_format: str = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format: table, json, or sarif.",
    ),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Write output to a file."),
    fail_on: Optional[str] = typer.Option(None, "--fail-on", help="Minimum severity that fails."),
    warn_on: Optional[str] = typer.Option(None, "--warn-on", help="Minimum severity that warns."),
    no_color: bool = typer.Option(False, "--no-color", help="Disable color output."),
) -> None:
    """Run one rule against one file for pack authoring and debugging."""

    config_path, repo_config, orchestrator = _load_scan_context(file, pack, config, no_config)
    if not any(rule.id == rule_id for rule in orchestrator.rules):
        raise typer.BadParameter(f"Unknown rule: {rule_id}")

    ignored_rules = tuple(rule.id for rule in orchestrator.rules if rule.id != rule_id)
    summary = orchestrator.scan_paths(
        [file],
        fail_on=(fail_on or repo_config.thresholds.fail_on),
        warn_on=(warn_on or repo_config.thresholds.warn_on),
        ignore=DEFAULT_IGNORES + repo_config.ignore.paths,
        ignored_rules=ignored_rules,
        languages=repo_config.languages,
        config_path=str(config_path) if config_path else None,
    )
    rendered = _render(summary, output_format)
    _write_or_echo(rendered, output)

    raise typer.Exit(code=1 if summary.overall_status == "FAIL" else 0)


@app.command("init")
def init_config(path: Path = typer.Option(Path("anaya.yml"), "--path", help="Config path.")) -> None:
    """Create a starter anaya.yml file."""

    if path.exists():
        raise typer.BadParameter(f"{path} already exists")
    path.write_text(
        "\n".join(
            [
                'version: "1"',
                "",
                "packs:",
                *[f"  - id: {pack_id}" for pack_id in DEFAULT_PACKS],
                "",
                "scan:",
                "  mode: diff",
                "  languages: []",
                "",
                "thresholds:",
                "  fail_on: CRITICAL",
                "  warn_on: HIGH",
                "",
                "ignore:",
                "  paths:",
                '    - "tests/**"',
                '    - "node_modules/**"',
                '    - "vendor/**"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    typer.echo(f"Created {path}")


@app.command("validate-pack")
def validate_pack(path: Path) -> None:
    """Validate a rule pack YAML file."""

    errors = validate_rule_pack(path)
    if errors:
        for error in errors:
            typer.echo(error, err=True)
        raise typer.Exit(code=1)
    typer.echo(f"{path} is valid")


@packs_app.command("list")
def list_packs() -> None:
    """List bundled rule packs."""

    for path in built_in_pack_paths():
        pack = load_rule_pack(path)
        typer.echo(f"{pack.id} {pack.version} - {len(pack.rules)} rule(s)")


def _load_scan_context(
    path: Path,
    pack: Optional[list[str]],
    config: Optional[Path],
    no_config: bool,
) -> tuple[Path | None, RepositoryConfig, ScanOrchestrator]:
    config_path = None if no_config else (config if config is not None else find_config(path))
    try:
        repo_config = load_repository_config(config_path)
        pack_ids = tuple(pack) if pack else repo_config.packs
        pack_base_dir = None if pack else (config_path.parent if config_path else None)
        pack_paths = [resolve_pack_identifier(item, base_dir=pack_base_dir) for item in pack_ids]
        orchestrator = ScanOrchestrator.from_pack_paths(pack_paths)
    except (FileNotFoundError, RepositoryConfigError, RulePackError) as exc:
        raise typer.BadParameter(str(exc)) from exc
    return config_path, repo_config, orchestrator


def _write_or_echo(rendered: str, output: Path | None) -> None:
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    else:
        typer.echo(rendered)


def _render(summary, output_format: str) -> str:
    normalized = output_format.lower()
    if normalized == "table":
        return format_table(summary)
    if normalized == "json":
        return format_json(summary)
    if normalized == "sarif":
        return format_sarif(summary)
    raise typer.BadParameter("format must be one of: table, json, sarif")


if __name__ == "__main__":
    app()
