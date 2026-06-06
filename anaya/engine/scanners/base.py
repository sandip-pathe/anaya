"""Scanner interface shared by concrete scanner implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from anaya.engine.models import Rule, Violation


class Scanner(ABC):
    """Base class for Anaya scanners."""

    @abstractmethod
    def scan_file_content(
        self,
        file_path: str,
        content: str,
        rules: list[Rule],
    ) -> list[Violation]:
        """Scan one file's content and return violations."""
