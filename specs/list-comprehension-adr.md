# ADR: List Comprehension

**Status**: Accepted · **Spec**: `specs/list-comprehension.md`

## Context
Show idiomatic comprehensions and their scoping pitfalls.

## Decision
Single module `src/04_list_comprehension/main.py` (stdlib only) with a `solve(text) -> str` adapter for the `tests/04_list_comprehension/NNN.in`/`.out` format; `tests/04_list_comprehension/test.py` runs the data-driven cases plus direct unit tests. Each helper is one comprehension or generator expression; `sum_squares_lazy` passes a generator to `sum`; `late_binding_bug` returns lambdas that all return 2; fixed with a default argument (`lambda i=i: i`).

## Alternatives considered
- `map`/`filter`: less readable.
- Loops: contradict the task (single comprehension).

## Consequences
- `transpose` uses `zip(*matrix)`, so ragged rows are truncated to the shortest.
- `invert` loses data if values repeat.

## Risks / gaps
None.
