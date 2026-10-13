# Spec: Class Inheritance

**Feature Slug**: `class-inheritance`
**Status**: Draft (drafted by Claude from `src/06_class_inheritance/task-en.md`; pending user review)

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

Inheritance mechanics: abstract bases, `super()`, MRO and diamonds, mixins, class vs instance attributes, and `__init_subclass__` registries.

---

## Requirements

- As a developer, I want abstract shapes and a diamond hierarchy so that I can explain `super()` and MRO.
- As a developer, I want a mixin and a subclass registry so that I can show composition patterns.

---

## Acceptance Criteria

- [ ] `Shape` is abstract (instantiation raises `TypeError`); `Circle(r)`, `Rectangle(w, h)` and `Square(side)` (calls `super().__init__(side, side)`) implement `area()`; `total_area(shapes)` sums areas.
- [ ] `describe()` chained with `super()` returns `"Shape Rectangle Square"` for `Square`.
- [ ] Diamond `A, B(A), C(A), D(B, C)`: `hello()` returns a list of class names with each class exactly once (`D().hello() == ["D","B","C","A"]`); `diamond_mro()` returns `["D","B","C","A","object"]`.
- [ ] `JsonMixin.to_json()` returns `json.dumps(vars(self))`; `Point(x, y)` uses it.
- [ ] `Counter`: class attribute `created` counts instances created, instance attribute `n` (bumped by `bump()`) is per-object.
- [ ] `Animal.__init_subclass__` registers every subclass in `Animal.registry` by class name; `Dog().speak() == "Woof"`, `Cat().speak() == "Meow"`; `Animal().speak()` raises `NotImplementedError`; an unregistered name lookup raises `KeyError`.
- [ ] `solve(text)` handles `area rect W H|square S|circle R|shape`, `describe ...`, `mro CLASS`, `hello CLASS`, `speak NAME` (looks up `NAME.capitalize()` in the registry); `area`/`describe` args are integers; `mro`/`hello` take a class name from module globals. Output is `str()` of the result (`mro`/`hello` space-joined) or the exception class name.

---

## Test Approach

**Primary approach**: Unit, data-driven (`tests/06_class_inheritance/NNN.in` -> `NNN.out` via `solve(text)`) plus direct tests of the functions that the text format cannot express.

**What not to test**: Python's own language behavior beyond the criteria.

**Run command**: `python3 -m unittest discover -s tests/06_class_inheritance`

---

## Smoke Test

- **Start command**: `cd src/06_class_inheritance && python3 main.py < ../../tests/06_class_inheritance/001.in`
- **Expected result**: output equals `tests/06_class_inheritance/001.out`, exit code 0.
- **Failure this catches**: import error, broken `solve` entry point.

---

## Constraints

- Standard library only.
- `main.py` exposes `solve(text) -> str`.

---

## Out of Scope

- Anything not listed in the acceptance criteria.
