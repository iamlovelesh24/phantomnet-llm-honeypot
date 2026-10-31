"""
PhantomNet path safety utilities.

Member 2:
Generative FUSE Filesystem & Deception Shell

This module ensures that all filesystem paths remain inside
the controlled PhantomNet sandbox.
"""

from pathlib import Path


class PathGuard:
    """Prevent filesystem access outside the PhantomNet sandbox."""

    def __init__(self, sandbox_root: str | Path):
        self.sandbox_root = Path(sandbox_root).resolve()

    def resolve(self, requested_path: str | Path) -> Path:
        """
        Resolve a requested path and ensure it stays inside the sandbox.

        Raises:
            PermissionError: If the requested path attempts to escape
            the PhantomNet sandbox.
        """
        requested = Path(requested_path)

        # Convert relative paths to paths inside the sandbox.
        if not requested.is_absolute():
            requested = self.sandbox_root / requested

        resolved = requested.resolve()

        try:
            resolved.relative_to(self.sandbox_root)
        except ValueError as exc:
            raise PermissionError(
                f"Access denied: path is outside PhantomNet sandbox: "
                f"{requested_path}"
            ) from exc

        return resolved

    def is_safe(self, requested_path: str | Path) -> bool:
        """Return True when the requested path stays inside the sandbox."""
        try:
            self.resolve(requested_path)
            return True
        except PermissionError:
            return False