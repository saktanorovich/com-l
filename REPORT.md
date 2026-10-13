# Test Report

**Date**: 2026-10-12 · **Python**: 3.14.0 · **Framework**: unittest (stdlib)

## Result

All 8 suites pass: **304 tests, 0 failures, 0 errors.**

| Suite | Location | Tests | Result |
|---|---|---|---|
| 00 Countdown | `tests/00_countdown` | 11 | OK |
| 01 Iterator protocol | `tests/01_iterator_protocol` | 42 | OK |
| 02 Decorators | `tests/02_decorators` | 33 | OK |
| 03 Threading / GIL | `tests/03_threading_gil` | 37 | OK |
| 04 List comprehension | `tests/04_list_comprehension` | 29 | OK |
| 05 File handling | `tests/05_file_handling` | 58 | OK |
| 06 Class inheritance | `tests/06_class_inheritance` | 42 | OK |
| 07 List mutation | `tests/07_list_mutation` | 52 | OK |

Implementations live in `src/<same folder name>/main.py`.

## How to reproduce

```sh
sh tests/run_all.sh    # suites 00-07, each run separately
```

The topics are run one at a time because each defines a module named `main`, which would clash in a single discovery pass.

## Notes

- 00 and 01 were rebuilt spec-first (`specs/countdown-iterator.md`, `specs/iterator-protocol.md`); 02-07 were moved unchanged from `interview/` except for the path to `main.py` in each `test.py`.
- Spec and ADR paths were updated (at your request) to the current `src/<NN_topic>` and `tests/<NN_topic>` layout; the old `interview/` and hyphenated paths are gone.
- `install.sh` was removed; the README now documents manual installation.
- No team-mode review (tech-lead `REVIEW.md`) was run; the work was done in single-agent mode.
