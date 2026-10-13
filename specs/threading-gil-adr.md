# ADR: Threading and the GIL

**Status**: Accepted · **Spec**: `specs/threading-gil.md`

## Context
Contrast threads (I/O-bound), processes (CPU-bound) and locks; results must be deterministic for tests.

## Decision
Single module `src/03_threading_gil/main.py` (stdlib only) with a `solve(text) -> str` adapter for the `tests/03_threading_gil/NNN.in`/`.out` format; `tests/03_threading_gil/test.py` runs the data-driven cases plus direct unit tests. `threading.Lock` in `SafeCounter`; `ThreadPoolExecutor.map` for I/O; `ProcessPoolExecutor.map` for CPU with a top-level picklable helper `sum_of_squares`; `queue.Queue` with a single private `object()` sentinel put once per consumer (the `producer_consumer` docstring still says `None`; stale wording, behavior is the private sentinel); `dis.Bytecode` for the atomicity demo.

## Alternatives considered
- `multiprocessing.Pool`: equivalent, executors give a uniform API.
- `None` as sentinel: rejected, a legitimate item could be `None`.
- `asyncio`: out of scope.

## Consequences
- Process pools cost startup time; tests use small inputs. Default workers: 8 (I/O), 2 (CPU).
- `workers < 1` raises `ValueError` from the executor.
- Callables for `parallel_map_cpu` must be picklable (module-level).

## Risks / gaps
Bytecode output is CPython-version specific; tests assert only that it contains `LOAD` and `STORE`.
- `producer_consumer` result order is nondeterministic with several consumers; `solve` sorts it.
