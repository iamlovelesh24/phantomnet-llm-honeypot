"""
PhantomNet synthetic file generator.

Generates deterministic-looking fake corporate files for the
controlled deception environment.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from hashlib import sha256
from typing import Dict
from urllib.request import Request, urlopen


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

    _SAFE_FILENAME = re.compile(
        r"^[A-Za-z0-9][A-Za-z0-9_-]{0,47}\.txt$",
        re.IGNORECASE,
    )

    _BLOCKED_FILENAMES = {
        "secret_keys.txt",
        "credentials.txt",
        "passwords.txt",
        "api_keys.txt",
    }

    def __init__(self, session_id: str = "session-demo"):
        self.session_id = session_id
        self._cache: Dict[str, GeneratedFile] = {}
        self._listing_cache: Dict[str, list[str]] = {}

        self._ollama_base_url = os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434"
        ).rstrip("/")
        self._ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        self._ollama_available = (
            os.getenv("PHANTOMNET_ENABLE_OLLAMA", "true").lower()
            not in {"0", "false", "no"}
        )

        try:
            self._ollama_timeout = min(
                max(float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "1")), 0.1),
                3.0,
            )
        except ValueError:
            self._ollama_timeout = 1.0

    def list_files(self, directory: str) -> list[str]:
        """Return validated, cached filenames with predefined fallback."""
        directory = directory.strip("/")

        if directory not in self.DIRECTORIES:
            return []

        if directory in self._listing_cache:
            return list(self._listing_cache[directory])

        # Always retain the known, safe filenames.
        names = list(self.DIRECTORIES[directory])

        if self._ollama_available:
            try:
                candidates = self._request_ollama_filenames(directory)
            except (OSError, ValueError, KeyError, TypeError):
                # Avoid repeated connection delays when Ollama is unavailable.
                self._ollama_available = False
                candidates = []

            seen = {name.casefold() for name in names}
            added = 0

            for candidate in candidates:
                if not isinstance(candidate, str):
                    continue

                filename = candidate.strip().strip("`").strip()

                if not self._SAFE_FILENAME.fullmatch(filename):
                    continue

                if filename.casefold() in self._BLOCKED_FILENAMES:
                    continue

                if filename.casefold() in seen:
                    continue

                names.append(filename)
                seen.add(filename.casefold())
                added += 1

                if added >= 3:
                    break

        self._listing_cache[directory] = names
        return list(names)

    def _request_ollama_filenames(self, directory: str) -> list:
        """Ask the local Ollama API for additional fictional filenames."""
        existing = ", ".join(self.DIRECTORIES[directory])
        prompt = (
            "Generate exactly three additional fictional corporate document "
            "filenames for a cybersecurity deception filesystem. "
            f"Department: {directory}. Existing filenames: {existing}. "
            "Return only a JSON array of simple .txt filenames. "
            "Do not include paths, directories, credentials, passwords, "
            "API keys, or Markdown."
        )

        payload = {
            "model": self._ollama_model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        request = Request(
            f"{self._ollama_base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=self._ollama_timeout) as response:
            envelope = json.loads(response.read().decode("utf-8"))

        parsed = json.loads(envelope.get("response", "[]"))

        if isinstance(parsed, dict):
            parsed = parsed.get("filenames", [])

        if not isinstance(parsed, list):
            raise ValueError("Ollama returned an invalid filename list")

        return parsed

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