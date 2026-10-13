# Iterator Protocol

Implement in `main.py`:

1. `Countdown(start)` - a class-based **iterator** yielding `start, start-1, ..., 1`, then raising `StopIteration`. `iter(c) is c`.
2. `CountdownIterable(start)` - an **iterable** that can be looped over any number of times.
3. `fibonacci(n)` - a lazy generator of the first `n` Fibonacci numbers.
4. `chunked(iterable, size)` - yield lists of `size` items (last may be shorter); must work with one-shot iterators; `size < 1` -> `ValueError`.
5. `manual_for_loop(iterable)` - collect items using only `iter()`, `next()` and `StopIteration` (what `for` does under the hood).

## Test data format (`tests/01_iterator_protocol/data/NNN.in` -> `tests/01_iterator_protocol/data/NNN.out`)

Each line is one command: `fib N` | `countdown N` | `chunk SIZE item...`. Output is the Python repr of the resulting list, or the exception class name (e.g. `ValueError`).
`main.py` exposes `solve(text) -> str`; `python3 src/01_iterator_protocol/main.py < tests/01_iterator_protocol/data/001.in` prints the answer.

Run (from the repo root): `python3 -m unittest discover -s tests/01_iterator_protocol`
