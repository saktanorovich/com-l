# Spec: Iterator Protocol

**Feature Slug**: `iterator-protocol`
**Status**: Draft (drafted by Claude from `src/01_iterator_protocol/task-en.md`; pending user review)

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

Hand-written iterators and generators that demonstrate Python's iterator protocol (`__iter__`/`__next__`/`StopIteration`), and the difference between an iterator and an iterable.

---

## Requirements

- As a developer, I want a class-based iterator and a re-usable iterable so that I can show the exhausted-iterator gotcha.
- As a developer, I want lazy generators and a chunker that works on one-shot iterators so that large data is processed in O(1) memory.
- As a developer, I want a manual `for` loop so that I can show what `for` does under the hood.

---

## Acceptance Criteria

- [ ] `Countdown(start)` yields `start..1`, then raises `StopIteration` (and keeps raising); `start <= 0` yields nothing; `iter(c) is c`; a second pass over the same instance yields nothing.
- [ ] `CountdownIterable(start)` can be looped any number of times with the same result.
- [ ] `fibonacci(n)` lazily yields the first `n` Fibonacci numbers starting `0, 1, 1, 2, ...`; `n <= 0` yields nothing.
- [ ] `chunked(iterable, size)` yields lists of `size` (last may be shorter), consumes the source lazily, keeps falsy items, and works with one-shot iterators and empty input.
- [ ] `chunked` with `size < 1` raises `ValueError` when the generator is first advanced (it is a generator function, so not at call time).
- [ ] `manual_for_loop(iterable)` collects items using only `iter()`, `next()` and `StopIteration`; a non-iterable raises `TypeError`.
- [ ] `solve(text)` handles commands `fib N`, `countdown N`, `chunk SIZE item...`; each input line yields one output line: `str()` of the resulting list (`chunk` items stay strings) or the exception class name; output ends with a newline.

---

## Test Approach

**Primary approach**: Unit, data-driven (`tests/01_iterator_protocol/data/NNN.in` -> `NNN.out` via `solve(text)`) plus direct tests of the functions that the text format cannot express.

**What not to test**: Python's own language behavior beyond the criteria.

**Run command**: `python3 -m unittest discover -s tests/01_iterator_protocol`

---

## Smoke Test

- **Start command**: `cd src/01_iterator_protocol && python3 main.py < ../../tests/01_iterator_protocol/data/001.in`
- **Expected result**: output equals `tests/01_iterator_protocol/data/001.out`, exit code 0.
- **Failure this catches**: import error, broken `solve` entry point.

---

## Constraints

- Standard library only.
- `main.py` exposes `solve(text) -> str`.

---

## Out of Scope

- Anything not listed in the acceptance criteria.
