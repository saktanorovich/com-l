# Spec: Decorators

**Feature Slug**: `decorators`
**Status**: Draft (drafted by Claude from `src/02_decorators/task-en.md`; pending user review)

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

Decorator patterns: simple, factory (with arguments), caching, timing, and stacking order.

---

## Requirements

- As a developer, I want decorators that preserve function metadata so that introspection and debugging keep working.
- As a developer, I want a retry factory and a memoizer so that I can show cross-cutting concerns.

---

## Acceptance Criteria

- [ ] `call_counter` exposes `.calls` (starts at 0, incremented on every call) and preserves `__name__` and `__doc__` (`functools.wraps`).
- [ ] `retry(times, exceptions=(Exception,))` retries only the given exceptions, calls the function at most `times` times, re-raises the last exception after the final attempt, and lets other exceptions propagate immediately.
- [ ] `retry(times, ...)` with `times < 1` raises `ValueError` when the factory is called (before decorating).
- [ ] `memoize` caches by positional and keyword arguments (kwargs order-insensitive); arguments must be hashable and sortable by key.
- [ ] `timed` stores the last run time in `.last_duration` (`None` before the first call), even if the function raises.
- [ ] `stacking_order()` returns `["outer", "inner"]`.
- [ ] `solve(text)`: `fib N` prints `<value> <real computations>`; `retry TIMES FAILS` prints `ok <attempts>` or `ValueError <attempts>` (just `ValueError` if `TIMES < 1`).

---

## Test Approach

**Primary approach**: Unit, data-driven (`tests/02_decorators/NNN.in` -> `NNN.out` via `solve(text)`) plus direct tests of the functions that the text format cannot express.

**What not to test**: Python's own language behavior beyond the criteria.

**Run command**: `python3 -m unittest discover -s tests/02_decorators`

---

## Smoke Test

- **Start command**: `cd src/02_decorators && python3 main.py < ../../tests/02_decorators/001.in`
- **Expected result**: output equals `tests/02_decorators/001.out`, exit code 0.
- **Failure this catches**: import error, broken `solve` entry point.

---

## Constraints

- Standard library only.
- `main.py` exposes `solve(text) -> str`.

---

## Out of Scope

- Anything not listed in the acceptance criteria.
