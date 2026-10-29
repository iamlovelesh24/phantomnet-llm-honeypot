# PhantomNet Generative FUSE Filesystem

**Owner:** Member 2 — Generative FUSE Filesystem & Deception Shell

## 1. Overview

PhantomNet provides a virtual filesystem with synthetic corporate directories
and on-demand file content for a controlled cybersecurity deception environment.

## 2. Virtual Directory Structure

The mount point is `~/phantomnet_mount`.

| Path | Purpose |
|---|---|
| `/HR` | Synthetic employee and benefits files |
| `/Finance` | Synthetic budgets, reports, and invoices |
| `/Engineering` | Synthetic projects and technical documents |
| `/Mail` | Synthetic inbox and internal communications |
| `/secret_keys.txt` | Simulated secret-store deception scenario |

All generated content and credentials are fictional.

## 3. Content Generation and Identity

- `deception/file_generator.py` generates synthetic corporate content.
- Each generated record exposes a `file_id`.
- The file identifier depends on the session ID and file path.
- Repeated access within a session produces consistent content and identity.
- Different sessions produce different identifiers for the same path.
- Generated records are cached within the generator instance.
- `deception/scenarios.py` supplies the synthetic secret-store content.

## 4. Sandbox Safety

`deception/path_guard.py` validates paths against the configured sandbox root.
Unsafe paths are rejected, and the FUSE layer converts rejected access into
permission errors.

Unknown files are rejected instead of being read from the host filesystem.
Never include real credentials, production secrets, or confidential company data.

## 5. Running and Testing

From the repository root, activate the project virtual environment and start
the filesystem with `python -m deception.fuse_fs`.

Keep the filesystem server running in the first terminal. Use a second terminal
to inspect `~/phantomnet_mount`, list its directories, and read synthetic files.

Example commands: `ls ~/phantomnet_mount`,
`ls ~/phantomnet_mount/HR`,
`cat ~/phantomnet_mount/HR/employees.txt`, and
`cat ~/phantomnet_mount/secret_keys.txt`.

Stop the foreground filesystem process with `Ctrl+C`.

Run automated tests using `python -m pytest -q tests/test_fuse_fs.py`.
The latest recorded result was **11 passed**.

The tests cover directory listing, file access, metadata, unknown files,
path traversal protection, synthetic secret-store content, and session/file
identifier consistency.

## 6. Read-Latency Benchmark

Run `python tests/benchmark_fuse_fs.py` while the FUSE filesystem is mounted.
The benchmark performs five warm-up reads followed by 100 measured reads
for each of the two files below.

| Metric | HR file | Secret file |
|---|---:|---:|
| Average | 0.413 ms | 0.412 ms |
| Median | 0.388 ms | 0.389 ms |
| P95 | 0.523 ms | 0.505 ms |
| Minimum | 0.354 ms | 0.353 ms |
| Maximum | 0.644 ms | 0.794 ms |

The measured average read latency was below 500 ms for both files. The P95
results were slightly above 500 ms.

These measurements represent warmed, mounted-file reads. Operating-system
caching can affect results; the benchmark does not measure cold reads, live
LLM generation, or end-to-end application latency.

## 7. Integration Status

The current implementation uses predefined virtual directories and synthetic
content generation. Integration with the Ollama lore/context engine and the
other PhantomNet services still requires separate verification.
