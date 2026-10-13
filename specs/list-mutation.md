# Spec: List Mutation (Shallow Copy)

**Feature Slug**: `list-mutation`
**Status**: Draft (drafted by Claude from `src/07_list_mutation/task-en.md`; pending user review)

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

Aliasing, shallow vs deep copy and common list-mutation bugs, each with a buggy and a fixed version.

---

## Requirements

- As a developer, I want buggy/fixed pairs so that I can explain each pitfall.

---

## Acceptance Criteria

- [ ] `alias(a) is a`; `shallow` and `slice_copy` return a new outer list with the same inner objects; `deep` returns fully independent copies; `shares_inner_objects(a, b)` is `True` if any pair `a[i] is b[i]`.
- [ ] `grid_buggy` (`[[0]*c]*r`) shares rows; `grid_fixed` does not.
- [ ] `append_buggy` leaks state through a mutable default argument; `append_fixed` does not.
- [ ] `remove_evens_buggy` mutates and returns its argument and skips elements (e.g. `[2,4,6]` -> `[4]`); `remove_evens_fixed` returns a new list of odds; `remove_evens_inplace` keeps identity via `nums[:] = ...`.
- [ ] `iadd_vs_add()` returns `(True, False)`.
- [ ] `sort_vs_sorted(nums)` returns `(sorted_list, original_list_unchanged, None)`: a new sorted list, an untouched copy of the input order, and `None` (the return value of `list.sort()`).
- [ ] `solve(text)` handles `evens`, `evens_buggy`, `grid_fixed R C`, `grid_buggy R C`, `shallow_append X`, `deep_append X`, `sort n...`, `iadd`; `grid_*` set `[0][0] = 1` on a non-empty grid before printing; `shallow_append`/`deep_append` append to the first inner list of `[[1],[2]]` via the copy and print the original; output is `str()` of the result.

---

## Test Approach

**Primary approach**: Unit, data-driven (`tests/07_list_mutation/NNN.in` -> `NNN.out` via `solve(text)`) plus direct tests of the functions that the text format cannot express.

**What not to test**: Python's own language behavior beyond the criteria.

**Run command**: `python3 -m unittest discover -s tests/07_list_mutation`

---

## Smoke Test

- **Start command**: `cd src/07_list_mutation && python3 main.py < ../../tests/07_list_mutation/001.in`
- **Expected result**: output equals `tests/07_list_mutation/001.out`, exit code 0.
- **Failure this catches**: import error, broken `solve` entry point.

---

## Constraints

- Standard library only.
- `main.py` exposes `solve(text) -> str`.

---

## Out of Scope

- Anything not listed in the acceptance criteria.
