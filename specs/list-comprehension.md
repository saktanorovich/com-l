# Spec: List Comprehension

**Feature Slug**: `list-comprehension`
**Status**: Draft (drafted by Claude from `src/04_list_comprehension/task-en.md`; pending user review)

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

Idiomatic list, dict and set comprehensions and generator expressions, plus scoping and closure pitfalls.

---

## Requirements

- As a developer, I want each helper written as one comprehension so that I can show idiomatic Python.
- As a developer, I want the scope and late-binding pitfalls demonstrated so that I can explain them.

---

## Acceptance Criteria

- [ ] `squares_of_evens(nums)` (any iterable), `flatten(nested)` (one level) and `transpose(matrix)` (list of row lists; rows truncated to the shortest) return correct results.
- [ ] `word_lengths(words)` is a dict comprehension; `invert(d)` swaps keys/values; `unique_lengths(words)` is a set comprehension.
- [ ] `pairs_with_sum(nums, target)` returns a list of `(nums[i], nums[j])` tuples with `i < j` summing to `target`.
- [ ] `fizzbuzz(n)` returns the list of strings for 1..n (`"FizzBuzz"`, `"Fizz"`, `"Buzz"`, or the number as text).
- [ ] `sum_squares_lazy(n)` equals the sum of `i*i` for `i in range(n)` with no intermediate list.
- [ ] `loop_var_does_not_leak()` returns `True` (comprehension variable raises `NameError` outside).
- [ ] `late_binding_bug()` returns 3 lambdas that all return `2`; `late_binding_fixed()` returns 3 lambdas returning `0, 1, 2`.
- [ ] `solve(text)` handles `fizzbuzz N`, `squares n...`, `lengths word...`, `pairs TARGET n...`, `transpose 1,2;3,4`; output is the repr of the result.

---

## Test Approach

**Primary approach**: Unit, data-driven (`tests/04_list_comprehension/NNN.in` -> `NNN.out` via `solve(text)`) plus direct tests of the functions that the text format cannot express.

**What not to test**: Python's own language behavior beyond the criteria.

**Run command**: `python3 -m unittest discover -s tests/04_list_comprehension`

---

## Smoke Test

- **Start command**: `cd src/04_list_comprehension && python3 main.py < ../../tests/04_list_comprehension/001.in`
- **Expected result**: output equals `tests/04_list_comprehension/001.out`, exit code 0.
- **Failure this catches**: import error, broken `solve` entry point.

---

## Constraints

- Standard library only.
- `main.py` exposes `solve(text) -> str`.

---

## Out of Scope

- Anything not listed in the acceptance criteria.
