# ADR: List Mutation (Shallow Copy)

**Status**: Accepted · **Spec**: `specs/list-mutation.md`

## Context
Show aliasing and mutation pitfalls with paired buggy/fixed code.

## Decision
Single module `src/07_list_mutation/main.py` (stdlib only) with a `solve(text) -> str` adapter for the `tests/07_list_mutation/NNN.in`/`.out` format; `tests/07_list_mutation/test.py` runs the data-driven cases plus direct unit tests. Buggy variants are kept intentionally and documented; fixed variants use new lists, `copy.deepcopy`, `None` default, and `nums[:] = ...`; `remove_evens_buggy` mutates and returns its argument; `sort_vs_sorted` returns `(sorted, copy of original, None)`; `solve` exercises both.

## Alternatives considered
- Removing buggy code: loses the teaching value.

## Consequences
- Buggy functions must never be used outside tests/demos.

## Risks / gaps
Buggy outputs depend on CPython iteration behavior; tests pin them.
