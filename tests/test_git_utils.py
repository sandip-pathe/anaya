import subprocess
from pathlib import Path

import pytest

from anaya.engine.git_utils import GitDiffError, changed_files_since


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


def test_changed_files_since_returns_modified_files(tmp_path: Path):
    _git(tmp_path, "init", "-b", "main")
    _git(tmp_path, "config", "user.email", "test@example.com")
    _git(tmp_path, "config", "user.name", "Test User")
    source = tmp_path / "source.py"
    source.write_text("print('a')\n", encoding="utf-8")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-m", "initial")
    source.write_text("print('b')\n", encoding="utf-8")

    changed = changed_files_since("HEAD", cwd=tmp_path)

    assert changed == [Path("source.py")]


def test_changed_files_since_raises_for_invalid_ref(tmp_path: Path):
    _git(tmp_path, "init", "-b", "main")

    with pytest.raises(GitDiffError):
        changed_files_since("missing-ref", cwd=tmp_path)
