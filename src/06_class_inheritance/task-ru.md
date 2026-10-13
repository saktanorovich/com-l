# Наследование классов

Реализуйте в `main.py`:

1. Абстрактный `Shape` (нельзя инстанцировать), `Circle`, `Rectangle`, `Square(Rectangle)` с использованием `super().__init__`; `total_area(shapes)`; `describe()` в цепочке через `super()` -> `"Shape Rectangle Square"`.
2. Ромб `A, B(A), C(A), D(B, C)`: кооперативный `hello()`, вызывающий каждый класс ровно один раз через `super()`; `diamond_mro()` возвращает имена классов.
3. `JsonMixin` + `Point` - `to_json()`.
4. `Counter` - атрибут класса `created` против атрибута экземпляра `n`.
5. `Animal` с реестром через `__init_subclass__`; `Dog`, `Cat`.

## Формат тестовых данных (`tests/06_class_inheritance/NNN.in` -> `tests/06_class_inheritance/NNN.out`)

Каждая строка: `area rect W H|square S|circle R|shape` | `describe ...` | `mro CLASS` | `hello CLASS` (A-D) | `speak animal`. Вывод - результат или имя класса исключения (`TypeError`, `KeyError`).
`main.py` предоставляет `solve(text) -> str`; `python3 src/06_class_inheritance/main.py < tests/06_class_inheritance/001.in` печатает ответ.

Запуск (из корня репозитория): `python3 -m unittest discover -s tests/06_class_inheritance`
