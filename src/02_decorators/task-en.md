# Decorators

Implement in `main.py`:

1. `call_counter` - exposes `.calls`; must preserve `__name__`/`__doc__` (`functools.wraps`).
2. `retry(times, exceptions)` - decorator **factory**; retries only on the given exceptions, re-raises after the last attempt.
3. `memoize` - cache by positional and keyword arguments.
4. `timed` - stores the last run time in `.last_duration`, even if the function raises.
5. `stacking_order()` - show that with `@outer @inner`, `outer`'s wrapper runs first. Return `["outer", "inner"]`.

Edge rule: `retry(times, ...)` with `times < 1` raises `ValueError`.

## Test data format (`tests/02_decorators/NNN.in` -> `tests/02_decorators/NNN.out`)

Each line: `fib N` prints `<value> <number of real computations>`; `retry TIMES FAILS` runs a function that fails `FAILS` times with `ValueError` and prints `ok <attempts>` or `ValueError <attempts>` (just `ValueError` if `TIMES < 1`).
`main.py` exposes `solve(text) -> str`; `python3 src/02_decorators/main.py < tests/02_decorators/001.in` prints the answer.

Run (from the repo root): `python3 -m unittest discover -s tests/02_decorators`
