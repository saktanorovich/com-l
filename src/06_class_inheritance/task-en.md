# Class Inheritance

Implement in `main.py`:

1. Abstract `Shape` (cannot be instantiated), `Circle`, `Rectangle`, `Square(Rectangle)` using `super().__init__`; `total_area(shapes)`; `describe()` chained with `super()` -> `"Shape Rectangle Square"`.
2. Diamond `A, B(A), C(A), D(B, C)`: cooperative `hello()` calling every class exactly once via `super()`; `diamond_mro()` returns class names.
3. `JsonMixin` + `Point` - `to_json()`.
4. `Counter` - class attribute `created` vs instance attribute `n`.
5. `Animal` with `__init_subclass__` registry; `Dog`, `Cat`.

## Test data format (`tests/06_class_inheritance/NNN.in` -> `tests/06_class_inheritance/NNN.out`)

Each line: `area rect W H|square S|circle R|shape` | `describe ...` | `mro CLASS` | `hello CLASS` (A-D) | `speak animal`. Output is the result or the exception class name (`TypeError`, `KeyError`).
`main.py` exposes `solve(text) -> str`; `python3 src/06_class_inheritance/main.py < tests/06_class_inheritance/001.in` prints the answer.

Run (from the repo root): `python3 -m unittest discover -s tests/06_class_inheritance`
