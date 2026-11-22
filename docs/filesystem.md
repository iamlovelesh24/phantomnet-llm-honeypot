# PhantomNet Generative FUSE Filesystem

**Owner:** Member 2 - Generative FUSE Filesystem & Deception Shell

## 1. Overview

PhantomNet provides a read-only virtual filesystem with synthetic corporate
directories and file content for a controlled cybersecurity deception
environment. Files use deterministic synthetic templates by default, with
optional LLM-generated content when explicitly enabled.

## 2. Virtual Directory Structure

The mount point is `~/phantomnet_mount`.

| Path | Purpose |
|---|---|
| `/HR` | Synthetic employee and benefits files |
| `/Finance` | Synthetic budgets, reports, and invoices |
| `/Engineering` | Synthetic projects and technical documents |
| `/Mail` | Synthetic inbox and internal communications |
| `/secret_keys.txt` | Predefined synthetic secret-store deception scenario |

All generated content and credentials are fictional.

## 3. Content Generation and Identity

- `deception/file_generator.py` generates synthetic corporate content.
- Each generated record exposes a `file_id`.
- The file identifier depends on the session ID and file path.
- Repeated access within a session produces consistent content and identity.
- Different sessions produce different identifiers for the same path.
- Generated records are cached within the generator instance.
- `deception/scenarios.py` supplies the synthetic secret-store content.
- The `/secret_keys.txt` file uses a predefined synthetic deception scenario.
- File contents use deterministic synthetic templates by default.
- Optional LLM-based file content generation can be enabled with
  `PHANTOMNET_ENABLE_LLM_CONTENT=true`.
- Optional LLM-generated content uses Member 1's prompt and context engine.
- Generated LLM content is validated against forbidden terms and registered
  employee and project IDs. Invalid or failed generation falls back to
  deterministic synthetic content.
- Department listings can request up to three additional filenames from Ollama.
- Generated names are validated and cached; invalid names are rejected.
- If Ollama is unavailable, predefined filenames remain available.

## 4. Sandbox Safety

`deception/path_guard.py` resolves requested paths and checks that they remain
inside the configured sandbox root. Unsafe paths raise `PermissionError`,
which the FUSE layer converts into access-denied errors (`EACCES`).

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
The previously recorded result was **17 passed**. The current test count
will be verified before this documentation is committed.

The tests cover directory listing, file access, metadata, unknown files,
path traversal protection, synthetic secret-store content, session/file
identifier consistency, dynamic filename validation, caching, fallback,
read-only access, and optional LLM content-generation integration.

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

Both average and P95 read latencies were below the project's 500 ms target in this local benchmark. The P95 values were 0.523 ms for the HR file and 0.505 ms for secret_keys.txt.

These measurements represent warmed, mounted-file reads. Operating-system
caching can affect results; the benchmark does not measure cold reads, live
LLM generation, or end-to-end application latency.

## 7. Optional Ollama Filename Generation

Department listings retain their predefined filenames and can request up to
three additional fictional filenames from the local Ollama API endpoint
`/api/generate`.

Configuration:

- `OLLAMA_BASE_URL`: defaults to `http://localhost:11434`
- `OLLAMA_MODEL`: defaults to `qwen2.5:7b`
- `OLLAMA_TIMEOUT_SECONDS`: defaults to 30 seconds, with a minimum of
  0.1 seconds and a maximum of 60 seconds
- `PHANTOMNET_ENABLE_OLLAMA=false`: disables Ollama filename generation

Model output is restricted to simple `.txt` filenames. Path-like names,
blocked credential-related filenames, duplicates, and unsupported filename
formats are rejected. Directory results are cached. If an API request fails,
the generator falls back to predefined filenames.

**Live verification:** Tested successfully with the Windows Ollama server
at `http://172.26.224.1:11434` and model `qwen2.5:7b`. The mounted FUSE HR
directory returned additional LLM-generated `.txt` filenames alongside
the predefined files.

Generated names can vary between generator instances. Listings are cached
within each FileGenerator instance. Automated tests also simulate Ollama
responses to validate filename filtering, caching, and fallback behavior.

LLM-generated filenames and LLM-generated file contents are separate
features. Filename generation is controlled by `PHANTOMNET_ENABLE_OLLAMA`,
while optional file-content generation is controlled by
`PHANTOMNET_ENABLE_LLM_CONTENT`.

Integration with the Ollama lore/context engine and the other PhantomNet
services still requires separate verification.
