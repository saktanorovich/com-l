# ADR: Class Inheritance

**Status**: Accepted · **Spec**: `specs/class-inheritance.md`

## Context
Demonstrate `super()`, MRO, mixins and registries.

## Decision
Single module `src/06_class_inheritance/main.py` (stdlib only) with a `solve(text) -> str` adapter for the `tests/06_class_inheritance/NNN.in`/`.out` format; `tests/06_class_inheritance/test.py` runs the data-driven cases plus direct unit tests. `abc.ABC` with `@abstractmethod` for `Shape`; every class in the diamond returns `[name] + super().hello()` (`A` ends the chain), giving `D, B, C, A`; `JsonMixin` uses `json.dumps(vars(self))`; `Animal.__init_subclass__` fills `Animal.registry` keyed by class name (same-named subclasses overwrite each other).

## Alternatives considered
- Explicit base calls (`B.hello(self)`): double-calls `A` in a diamond.
- Class decorator for registry: works, but `__init_subclass__` is the direct tool.

## Consequences
- Registry is global mutable state.
- `JsonMixin` serializes instance attributes only.

## Risks / gaps
None.
