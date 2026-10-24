"""
PhantomNet Generative FUSE Filesystem
Member 2 - Week 1

Week 1 scope:
- Create an isolated virtual filesystem
- Support directory listing
- Provide realistic synthetic directories/files
- No cat/file-content generation yet
"""

import errno
import os
from deception.file_generator import FileGenerator

try:
    from fuse import FUSE, Operations
except OSError:
    FUSE = None

    class Operations:
        pass


class PhantomNetFS(Operations):
    """Minimal PhantomNet filesystem for the Week 1 prototype."""
    def __init__(self):
        self.generator = FileGenerator()

    DIRECTORIES = {
        "/": ["HR", "Finance", "Engineering", "Mail"],
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

    def open(self, path, flags):
        """Allow read-only access to synthetic files."""
        if not self._is_file(path):
            raise OSError(errno.ENOENT, "No such file")

        return 0

    def read(self, path, size, offset, fh):
        """Generate and return synthetic file content on demand."""
        if not self._is_file(path):
            raise OSError(errno.ENOENT, "No such file")

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
            return {
                "st_mode": 0o644 | 0o100000,
                "st_nlink": 1,
                "st_size": len(self.generator.generate(path).content),
            }

        raise OSError(errno.ENOENT, "No such file or directory")

    def readdir(self, path, fh):
        """Return directory entries for ls."""
        if path not in self.DIRECTORIES:
            raise OSError(errno.ENOENT, "No such directory")

        yield "."
        yield ".."

        for name in self.DIRECTORIES[path]:
            yield name

    def _is_directory(self, path):
        return path in self.DIRECTORIES

    def _is_file(self, path):
        for directory, files in self.DIRECTORIES.items():
            for filename in files:
                expected_path = (
                    f"/{filename}"
                    if directory == "/"
                    else f"{directory}/{filename}"
                )

                if path == expected_path:
                    return True

        return False


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
