# Spec: File Handling and Resource Management

**Feature Slug**: `file-handling`
**Status**: Draft (drafted by Claude from `src/05_file_handling/task-en.md`; pending user review)

---

## Tech Stack

| Concern         | Choice             |
|-----------------|--------------------|
| Language        | Python             |
| Runtime/Version | Python 3.10+       |
| Framework       | none               |
| Test Framework  | unittest (stdlib)  |
| Package Manager | none (stdlib only) |

---

## Description

Safe, memory-bounded file handling: streaming reads, atomic writes and context managers.

---

## Requirements

- As a developer, I want streaming helpers so that large files are never fully loaded.
- As a developer, I want atomic writes and guaranteed closing so that failures never corrupt data or leak handles.

---

## Acceptance Criteria

- [ ] `count_lines(path)` returns the line count; `word_frequency(path)` returns a `dict` of lowercase whitespace-split words to counts; both stream the file line by line (UTF-8).
- [ ] `read_in_chunks(path, size=8192)` is a generator of text chunks of up to `size` characters.
- [ ] `atomic_write(path, content)` uses a temp file and `os.replace`; the temp file is created in the target's directory; on any failure (including `BaseException`) the old file stays and no temp file remains.
- [ ] `ManagedFile(path, mode="r")` (`__enter__` returns the file, `__exit__` closes it) closes the file even on exceptions and does not swallow them.
- [ ] `open_for_read(path)` behaves the same via `@contextlib.contextmanager`.
- [ ] `tail(path, n)` returns a list of the last `n` lines (trailing `\n` stripped) using a bounded deque.
- [ ] `copy_file(src, dst)` copies line by line, managing both files in one `with`.
- [ ] `solve(text)`: first line is the command (`count`, `words`, `tail N`, `chunks N`), the rest is file content; `words` prints sorted `word count` lines; `count` prints the line count; `chunks` prints the list of chunk lengths. `solve` writes the content to a temporary file and returns the output text.

---

## Test Approach

**Primary approach**: Unit, data-driven (`tests/05_file_handling/NNN.in` -> `NNN.out` via `solve(text)`) plus direct tests of the functions that the text format cannot express.

**What not to test**: Python's own language behavior beyond the criteria.

**Run command**: `python3 -m unittest discover -s tests/05_file_handling`

---

## Smoke Test

- **Start command**: `cd src/05_file_handling && python3 main.py < ../../tests/05_file_handling/001.in`
- **Expected result**: output equals `tests/05_file_handling/001.out`, exit code 0.
- **Failure this catches**: import error, broken `solve` entry point.

---

## Constraints

- Standard library only.
- `main.py` exposes `solve(text) -> str`.

---

## Out of Scope

- Anything not listed in the acceptance criteria.
