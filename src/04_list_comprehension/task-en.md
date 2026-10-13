# List Comprehension

Implement each in `main.py` as a single comprehension / generator expression:

1. `squares_of_evens(nums)`
2. `flatten(nested)` (one level)
3. `transpose(matrix)`
4. `word_lengths(words)` (dict comprehension)
5. `pairs_with_sum(nums, target)` - pairs `i < j` with the given sum
6. `fizzbuzz(n)` - list of strings for 1..n
7. `invert(d)`, `unique_lengths(words)` (set comprehension)
8. `sum_squares_lazy(n)` - sum of `i*i` for `i in range(n)` with no intermediate list
9. `loop_var_does_not_leak()` - prove comprehension scope
10. `late_binding_bug()` / `late_binding_fixed()` - closures in a comprehension

## Test data format (`tests/04_list_comprehension/NNN.in` -> `tests/04_list_comprehension/NNN.out`)

Each line: `fizzbuzz N` | `squares n...` | `lengths word...` | `pairs TARGET n...` | `transpose 1,2;3,4`. Output is the Python repr of the result.
`main.py` exposes `solve(text) -> str`; `python3 src/04_list_comprehension/main.py < tests/04_list_comprehension/001.in` prints the answer.

Run (from the repo root): `python3 -m unittest discover -s tests/04_list_comprehension`
