"""
PhantomNet synthetic file generator.

Generates deterministic-looking fake corporate files for the
controlled deception environment.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Dict


@dataclass(frozen=True)
class GeneratedFile:
    """Represents a synthetic PhantomNet file."""

    path: str
    content: str
    file_id: str


class FileGenerator:
    """Generate safe, synthetic corporate content."""

    DIRECTORIES = {
        "HR": [
            "employees.txt",
            "org_chart.txt",
            "benefits.txt",
        ],
        "Finance": [
            "quarterly_report.txt",
            "budget.txt",
            "invoices.txt",
        ],
        "Engineering": [
            "projects.txt",
            "deployment_notes.txt",
            "architecture.txt",
        ],
        "Mail": [
            "inbox.txt",
            "internal_memo.txt",
            "announcements.txt",
        ],
    }

    def __init__(self, session_id: str = "session-demo"):
        self.session_id = session_id
        self._cache: Dict[str, GeneratedFile] = {}

    def list_files(self, directory: str) -> list[str]:
        """Return synthetic filenames for a supported directory."""
        return list(self.DIRECTORIES.get(directory, []))

    def generate(self, path: str) -> GeneratedFile:
        """
        Generate deterministic synthetic content for a file.

        The same session and path produce the same content so that
        repeated access remains consistent.
        """
        if path in self._cache:
            return self._cache[path]

        seed = sha256(
            f"{self.session_id}:{path}".encode("utf-8")
        ).hexdigest()[:12]

        filename = path.rsplit("/", 1)[-1]
        file_id = f"PN-{seed.upper()}"

        content = (
            f"PHANTOMNET SYNTHETIC FILE\n"
            f"==========================\n"
            f"Session: {self.session_id}\n"
            f"File: {filename}\n"
            f"Reference: {file_id}\n\n"
            f"This content is synthetic and exists only inside the "
            f"PhantomNet deception environment.\n\n"
            f"Generated record:\n"
            f"- Department: {self._department(path)}\n"
            f"- Status: Internal Simulation\n"
            f"- Classification: Synthetic Demo Data\n"
        )

        generated = GeneratedFile(
            path=path,
            content=content,
            file_id=file_id,
        )

        self._cache[path] = generated
        return generated

    @staticmethod
    def _department(path: str) -> str:
        """Infer the synthetic department from the file path."""
        parts = path.strip("/").split("/")

        if parts:
            return parts[0]

        return "Unknown"