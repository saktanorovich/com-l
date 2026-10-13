# ADR: Countdown Iterator

**Status**: Accepted · **Spec**: `specs/countdown-iterator.md`

## Context
Teach the iterator protocol with the smallest possible example, including the exhausted-iterator gotcha.

## Decision
Single module `src/00_countdown/main.py` (stdlib only) exposing `Countdown` and a `solve(text) -> str` adapter for the `tests/00_countdown/data/NNN.in`/`.out` format. `Countdown` is a class holding a `current` counter; `__iter__` returns `self`; `__next__` raises `StopIteration` when `current <= 0`, otherwise returns the value and decrements. Tests live in `tests/00_countdown/` and load the module by file path (the slug contains a hyphen, so it is not importable by name).

## Alternatives considered
- Generator function for `Countdown`: shorter, but hides `__iter__`/`__next__`, which are the point of the exercise.
- `iter(range(start, 0, -1))`: correct but demonstrates nothing.

## Consequences
- `Countdown` is single-use by design: a second pass yields nothing.
- `start <= 0` is empty because the exhaustion check is `current <= 0`; no special case.
- Once exhausted, the counter never moves again, so `StopIteration` keeps being raised.

## Risks / gaps
None.
