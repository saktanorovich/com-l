# Spec: Threading and the GIL

**Feature Slug**: `threading-gil`
**Status**: Draft (drafted by Claude from `src/03_threading_gil/task-en.md`; pending user review)

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

Threads, processes and queues in Python, and why the GIL does not replace locks.

---

## Requirements

- As a developer, I want a thread-safe counter and ordered parallel maps so that I can contrast I/O-bound (threads) and CPU-bound (processes) work.
- As a developer, I want a queue pipeline and a bytecode demo so that I can explain races and sentinels.

---

## Acceptance Criteria

- [ ] `SafeCounter` (`increment()`, read-only `.value`, starts at 0, instances independent) with a `Lock`; `run_counter(counter, threads, increments)` returns `threads * increments` (0 for zero threads or zero increments).
- [ ] `parallel_map_io(func, items, workers=8)` keeps input order (even when early items are slow), accepts any iterable, and propagates exceptions; `workers < 1` raises `ValueError`.
- [ ] `parallel_map_cpu(func, items, workers=2)` uses a process pool (`func` must be picklable/top-level), keeps input order and propagates worker exceptions.
- [ ] `sum_of_squares(n)` is `sum(i*i for i in range(n))`, and `0` for `n <= 0`.
- [ ] `producer_consumer(items, consumers=4)` doubles every item via `queue.Queue`; each consumer is stopped by a private `object()` sentinel (so `None` items are safe); every item is processed exactly once; result order is not guaranteed with more than one consumer (`solve` sorts it).
- [ ] `producer_consumer` with `consumers < 1` raises `ValueError`.
- [ ] `why_increment_is_not_atomic()` returns the `dis` listing (string) of a function doing `global x; x += 1`, containing `LOAD` and `STORE` instructions.
- [ ] `solve(text)` handles `counter THREADS N`, `mapio WORKERS x...`, `cpu n...`, `pipe CONSUMERS x...`; output is `str()` of the result (`mapio` returns squares, `pipe` returns sorted doubles) or the exception class name.

---

## Test Approach

**Primary approach**: Unit, data-driven (`tests/03_threading_gil/NNN.in` -> `NNN.out` via `solve(text)`) plus direct tests of the functions that the text format cannot express.

**What not to test**: Python's own language behavior beyond the criteria.

**Run command**: `python3 -m unittest discover -s tests/03_threading_gil`

---

## Smoke Test

- **Start command**: `cd src/03_threading_gil && python3 main.py < ../../tests/03_threading_gil/001.in`
- **Expected result**: output equals `tests/03_threading_gil/001.out`, exit code 0.
- **Failure this catches**: import error, broken `solve` entry point.

---

## Constraints

- Standard library only.
- `main.py` exposes `solve(text) -> str`.

---

## Out of Scope

- Anything not listed in the acceptance criteria.
