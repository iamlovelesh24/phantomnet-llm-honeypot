"""Measure read latency through the mounted PhantomNet FUSE filesystem."""

import statistics
import time
from pathlib import Path

MOUNT_POINT = Path.home() / "phantomnet_mount"
ITERATIONS = 100

FILES = [
    MOUNT_POINT / "HR" / "employees.txt",
    MOUNT_POINT / "secret_keys.txt",
]


def benchmark(path: Path) -> None:
    if not path.is_file():
        print(f"SKIP: {path} is unavailable. Is FUSE mounted?")
        return

    # Warm-up reads are excluded from the measurements.
    for _ in range(5):
        path.read_bytes()

    timings_ms = []

    for _ in range(ITERATIONS):
        start = time.perf_counter()
        content = path.read_bytes()
        elapsed_ms = (time.perf_counter() - start) * 1000

        if not content:
            raise RuntimeError(f"Empty content returned by {path}")

        timings_ms.append(elapsed_ms)

    ordered = sorted(timings_ms)
    p95_index = max(0, int(0.95 * len(ordered)) - 1)

    print(f"\nFile: {path.relative_to(MOUNT_POINT)}")
    print(f"Iterations: {ITERATIONS}")
    print(f"Average: {statistics.mean(timings_ms):.3f} ms")
    print(f"Median:  {statistics.median(timings_ms):.3f} ms")
    print(f"P95:     {ordered[p95_index]:.3f} ms")
    print(f"Minimum: {min(timings_ms):.3f} ms")
    print(f"Maximum: {max(timings_ms):.3f} ms")


if __name__ == "__main__":
    if not MOUNT_POINT.is_dir():
        raise SystemExit(f"Mount point not found: {MOUNT_POINT}")

    for file_path in FILES:
        benchmark(file_path)
