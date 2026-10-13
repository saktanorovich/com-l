# Threading and the GIL

Implement in `main.py`:

1. `SafeCounter` - thread-safe counter (`increment()`, `.value`) using a `Lock`; `run_counter(counter, threads, increments)` runs it from many threads and returns the final value.
2. `parallel_map_io(func, items, workers)` - threaded map for I/O-bound work; keep input order, propagate exceptions.
3. `parallel_map_cpu(func, items, workers)` - same for CPU-bound work, bypassing the GIL via processes.
4. `producer_consumer(items, consumers)` - `queue.Queue` pipeline; each consumer doubles items; stop with sentinels.
5. `why_increment_is_not_atomic()` - return the `dis` bytecode of `x += 1` on a global to show why the GIL does not replace locks.

Edge rules: `producer_consumer(items, consumers)` with `consumers < 1` raises `ValueError` (a private sentinel, not `None`, stops consumers); `sum_of_squares(n)` is the CPU-bound helper (`sum(i*i for i in range(n))`, `0` for `n <= 0`).

## Test data format (`tests/03_threading_gil/NNN.in` -> `tests/03_threading_gil/NNN.out`)

Each line: `counter THREADS N` | `mapio WORKERS x...` (squares) | `cpu n...` (`sum_of_squares`) | `pipe CONSUMERS x...` (sorted doubles). Output is the result or the exception class name.
`main.py` exposes `solve(text) -> str`; `python3 src/03_threading_gil/main.py < tests/03_threading_gil/001.in` prints the answer.

Run (from the repo root): `python3 -m unittest discover -s tests/03_threading_gil`
