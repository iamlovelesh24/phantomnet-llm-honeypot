"""
PhantomNet Generative FUSE Filesystem
Member 2 - Week 2

Current scope:
- Isolated virtual filesystem
- Synthetic directory and file generation
- On-demand synthetic file content
- Path validation and sandbox protection
- Read-only deception filesystem behavior
"""

import errno
import os
from deception.file_generator import FileGenerator
from deception.path_guard import PathGuard
from deception.scenarios import get_scenario

try:
    from fuse import FUSE, Operations
except OSError:
    FUSE = None

    class Operations:
        pass


class PhantomNetFS(Operations):
    """PhantomNet read-only generative deception filesystem."""
    def __init__(self):
        self.generator = FileGenerator()
        self.path_guard = PathGuard("/tmp/phantomnet")

    DIRECTORIES = {
        "/": ["HR", "Finance", "Engineering", "Mail", "secret_keys.txt"],
        "/HR": [
            "employees.txt",
            "org_chart.txt",
            "benefits.txt",
        ],
        "/Finance": [
            "quarterly_report.txt",
            "budget.txt",
            "invoices.txt",
        ],
        "/Engineering": [
            "projects.txt",
            "deployment_notes.txt",
            "architecture.txt",
        ],
        "/Mail": [
            "inbox.txt",
            "internal_memo.txt",
            "announcements.txt",
        ],
    }

    def _validate_path(self, path):
        """Validate a virtual FUSE path against the PhantomNet sandbox."""
        try:
            virtual_path = str(path).lstrip("/")
            self.path_guard.resolve(virtual_path)
        except PermissionError as exc:
            raise OSError(errno.EACCES, str(exc)) from exc

    def open(self, path, flags):
        """Allow read-only access to synthetic files."""
        self._validate_path(path)

        if (flags & 3) != os.O_RDONLY:
            raise OSError(errno.EACCES, "PhantomNet filesystem is read-only")

        if not self._is_file(path):
            raise OSError(errno.ENOENT, "No such file")

        return 0

    def read(self, path, size, offset, fh):
        """Generate and return synthetic file content on demand."""
        self._validate_path(path)
        if not self._is_file(path):
            raise OSError(errno.ENOENT, "No such file")

        scenario = get_scenario(path.lstrip("/"))

        if scenario is not None:
            return scenario[offset:offset + size].encode("utf-8")

        generated = self.generator.generate(path)

        return generated.content[offset:offset + size].encode("utf-8")
    def getattr(self, path, fh=None):
        """Return basic filesystem metadata."""
        if path == "/" or self._is_directory(path):
            return {
                "st_mode": 0o755 | 0o040000,
                "st_nlink": 2,
            }

        if self._is_file(path):
            scenario = get_scenario(path.lstrip("/"))
            content = (
                scenario
                if scenario is not None
                else self.generator.generate(path).content
            )

            return {
                "st_mode": 0o644 | 0o100000,
                "st_nlink": 1,
                "st_size": len(content),
                "st_uid": getattr(os, "getuid", lambda: 0)(),
                "st_gid": getattr(os, "getgid", lambda: 0)(),
            }

        raise OSError(errno.ENOENT, "No such file or directory")

    def readdir(self, path, fh):
        """Return safe, cached filenames for directory listings."""
        if path not in self.DIRECTORIES:
            raise OSError(errno.ENOENT, "No such directory")

        yield "."
        yield ".."

        if path == "/":
            for name in self.DIRECTORIES["/"]:
                yield name
            return

        directory = path.strip("/")
        for name in self.generator.list_files(directory):
            yield name

    def _is_directory(self, path):
        return path in self.DIRECTORIES

    def _is_file(self, path):
        """Recognize predefined and validated generated synthetic files."""
        if path == "/secret_keys.txt":
            return True

        if not isinstance(path, str) or not path.startswith("/"):
            return False

        parts = path.strip("/").split("/")
        if len(parts) != 2:
            return False

        directory, filename = parts

        if directory not in self.generator.DIRECTORIES:
            return False

        return filename in self.generator.list_files(directory)


if __name__ == "__main__":
    if FUSE is None:
        print("FUSE runtime is unavailable on this system.")
        print("PhantomNet Week 1 filesystem logic can still be tested.")
    else:
        mount_point = os.path.expanduser("~/phantomnet_mount")

        os.makedirs(mount_point, exist_ok=True)

        print(f"Mounting PhantomNet filesystem at: {mount_point}")

        FUSE(
            PhantomNetFS(),
            mount_point,
            foreground=True,
        )
