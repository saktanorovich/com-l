# File Handling and Resource Management

Implement in `main.py`:

1. `count_lines(path)` and `word_frequency(path)` (case-insensitive) - stream, don't load the whole file.
2. `read_in_chunks(path, size)` - generator of chunks.
3. `atomic_write(path, content)` - temp file + `os.replace`; on failure the old file stays and no temp file remains.
4. `ManagedFile` - class-based context manager (`__enter__`/`__exit__`), closes on exceptions.
5. `open_for_read(path)` - the same via `@contextlib.contextmanager`.
6. `tail(path, n)` - last `n` lines with constant memory.
7. `copy_file(src, dst)` - two resources in one `with`.

## Test data format (`tests/05_file_handling/NNN.in` -> `tests/05_file_handling/NNN.out`)

The first line is the command (`count` | `words` | `tail N` | `chunks N`); the rest of the input is the content of the file to operate on. `words` prints `word count` lines sorted by word; `tail` prints the lines; `chunks` prints the list of chunk lengths.
`main.py` exposes `solve(text) -> str`; `python3 src/05_file_handling/main.py < tests/05_file_handling/001.in` prints the answer.

Run (from the repo root): `python3 -m unittest discover -s tests/05_file_handling`
