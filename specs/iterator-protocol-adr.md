# ADR: Iterator Protocol

**Status**: Accepted · **Spec**: `specs/iterator-protocol.md`

## Context
Teach the iterator protocol; code must be correct and show the exhausted-iterator gotcha.

## Decision
Single module `src/01_iterator_protocol/main.py` (stdlib only) with a `solve(text) -> str` adapter for the `tests/01_iterator_protocol/data/NNN.in`/`.out` format; `tests/01_iterator_protocol/test_iterator_protocol.py` runs the data-driven cases plus direct unit tests. `Countdown` is a class with `__iter__` returning self; `CountdownIterable` returns a fresh iterator each time; `fibonacci`/`chunked` are generators (`chunked` slices the source with a private `_take` helper in a walrus loop); `manual_for_loop` uses `iter`/`next`.

## Alternatives considered
- Generator for `Countdown`: shorter, but hides `__iter__`/`__next__`.
- `itertools.batched`/`islice` for `chunked`: batched needs 3.12; spec targets 3.10+.

## Consequences
- `Countdown` is single-use by design.
- `chunked` is a generator function, so `ValueError` for `size < 1` is raised on first advance, not at call time; tests consume it (e.g. via `list`).
- `Countdown` with `start <= 0` is empty.

## Risks / gaps
None.
