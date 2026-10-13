# List Mutation (Shallow Copy)

Implement in `main.py`:

1. `alias`, `shallow`, `deep`, `slice_copy`, `shares_inner_objects(a, b)`.
2. `grid_buggy` (`[[0]*c]*r`) vs `grid_fixed`.
3. `append_buggy` (mutable default arg) vs `append_fixed`.
4. `remove_evens_buggy` (mutating while iterating), `remove_evens_fixed` (new list), `remove_evens_inplace` (keeps identity via `nums[:] = ...`).
5. `iadd_vs_add()` -> `(True, False)`; `sort_vs_sorted(nums)` -> `(sorted_list, original_unchanged, None)`.

## Test data format (`tests/07_list_mutation/NNN.in` -> `tests/07_list_mutation/NNN.out`)

Each line: `evens n...` | `evens_buggy n...` | `grid_fixed R C` | `grid_buggy R C` (prints the grid after setting `[0][0] = 1`) | `shallow_append X` | `deep_append X` | `sort n...` | `iadd`. Output is the Python repr of the result.
`main.py` exposes `solve(text) -> str`; `python3 src/07_list_mutation/main.py < tests/07_list_mutation/001.in` prints the answer.

Run (from the repo root): `python3 -m unittest discover -s tests/07_list_mutation`
