# ADR: Decorators

**Status**: Accepted · **Spec**: `specs/decorators.md`

## Context
Show decorators that keep metadata and handle arguments, errors and state.

## Decision
Single module `src/02_decorators/main.py` (stdlib only) with a `solve(text) -> str` adapter for the `tests/02_decorators/NNN.in`/`.out` format; `tests/02_decorators/test.py` runs the data-driven cases plus direct unit tests. All decorators use `functools.wraps`; `retry` is a three-layer factory validating `times` when the factory is called (default `exceptions=(Exception,)`); `timed` uses `try/finally`; `memoize` keys on `(args, tuple(sorted(kwargs.items())))`.

## Alternatives considered
- `functools.lru_cache`: correct for production, hides the mechanism.
- Class-based decorators: heavier, no benefit here.

## Consequences
- `memoize` requires hashable arguments.
- Wrapper state (`.calls`, `.last_duration`) is not thread-safe.
- `memoize` cache is unbounded and per decorated function.

## Risks / gaps
Unhashable arguments to `memoize` raise `TypeError` (accepted).
