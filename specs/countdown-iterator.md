# Spec: Countdown Iterator

**Feature Slug**: `countdown-iterator`
**Status**: Draft (drafted by Claude from the `Countdown` criteria of `specs/iterator-protocol.md`; pending user review)

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

A hand-written, class-based iterator `Countdown` that demonstrates Python's iterator protocol (`__iter__` / `__next__` / `StopIteration`) and the exhausted-iterator gotcha.

---

## Requirements

- As a developer, I want a class-based iterator that counts down so that I can show what `__iter__` and `__next__` do.
- As a developer, I want the iterator to be single-use so that I can show the exhausted-iterator gotcha.

---

## Acceptance Criteria

- [ ] `Countdown(start)` yields `start, start-1, ..., 1`, then raises `StopIteration`.
- [ ] Once exhausted, every further `next()` keeps raising `StopIteration`.
- [ ] `start <= 0` (zero or negative) yields nothing.
- [ ] `iter(c) is c` (the iterator is its own iterator).
- [ ] A second pass over the same instance yields nothing (single-use).
- [ ] `solve(text)` handles lines of the form `countdown N`; each input line yields one output line: `str()` of the resulting list; output ends with a newline.

---

## Test Approach

**Primary approach**: Unit tests of `Countdown` plus data-driven tests (`tests/00_countdown/data/NNN.in` -> `NNN.out` via `solve(text)`).

**What not to test**: Python's own language behavior beyond the criteria.

**Run command**: `python3 -m unittest discover -s tests/00_countdown`

---

## Smoke Test

- **Start command**: `python3 src/00_countdown/main.py < tests/00_countdown/data/001.in`
- **Expected result**: output equals `data/001.out`, exit code 0.
- **Failure this catches**: import error, broken `solve` entry point.

---

## Constraints

- Standard library only.
- `src/00_countdown/main.py` exposes `Countdown` and `solve(text) -> str`.

---

## Out of Scope

- `CountdownIterable`, `fibonacci`, `chunked`, `manual_for_loop` (covered by `iterator-protocol`).
- Anything not listed in the acceptance criteria.
