"""Git helpers for diff-based scanning."""

from __future__ import annotations

from pathlib import Path
import subprocess


class GitDiffError(RuntimeError):
    """Raised when changed files cannot be resolved from Git."""


def changed_files_since(ref: str, cwd: str | Path = ".") -> list[Path]:
    """Return files changed since a Git ref, excluding deleted files."""

    command = ["git", "diff", "--name-only", "--diff-filter=ACMRT", ref, "--"]
    try:
        result = subprocess.run(
            command,
            cwd=Path(cwd),
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise GitDiffError(f"Could not determine changed files since {ref!r}") from exc

    return [Path(line.strip()) for line in result.stdout.splitlines() if line.strip()]
