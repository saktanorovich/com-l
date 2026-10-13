# ADR: File Handling and Resource Management

**Status**: Accepted · **Spec**: `specs/file-handling.md`

## Context
Handle files safely: bounded memory, no leaks, no partial writes.

## Decision
Single module `src/05_file_handling/main.py` (stdlib only) with a `solve(text) -> str` adapter for the `tests/05_file_handling/NNN.in`/`.out` format; `tests/05_file_handling/test.py` runs the data-driven cases plus direct unit tests. Iterate over the file object for streaming; `atomic_write` writes a temp file in the same directory then `os.replace` (temp from `tempfile.mkstemp(dir=<target dir>)`), removing the temp file in an `except BaseException` handler before re-raising; `tail` uses `collections.deque(maxlen=n)`; `ManagedFile.__exit__` returns `False` (never swallows) and the `@contextmanager` variant closes in `finally`; `word_frequency` lowercases and splits on whitespace; `solve` writes the content into a `TemporaryDirectory` file and runs the command on it.

## Alternatives considered
- `read().splitlines()`: simple but unbounded memory.
- `shutil.copyfile` for `copy_file`: correct in production, hides the two-resource `with`.
- `tempfile.NamedTemporaryFile` for the temp: not guaranteed same filesystem as target.
- `mkstemp` leaves the written file at mode 0600.

## Consequences
- `os.replace` is atomic only on the same filesystem (hence same-directory temp).
- Encoding fixed to UTF-8.

## Risks / gaps
Atomicity vs durability: no `fsync`; accepted for a demo.
