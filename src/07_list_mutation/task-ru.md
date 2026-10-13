# Изменение списков (поверхностное копирование)

Реализуйте в `main.py`:

1. `alias`, `shallow`, `deep`, `slice_copy`, `shares_inner_objects(a, b)`.
2. `grid_buggy` (`[[0]*c]*r`) против `grid_fixed`.
3. `append_buggy` (изменяемый аргумент по умолчанию) против `append_fixed`.
4. `remove_evens_buggy` (изменение при итерации), `remove_evens_fixed` (новый список), `remove_evens_inplace` (сохраняет идентичность через `nums[:] = ...`).
5. `iadd_vs_add()` -> `(True, False)`; `sort_vs_sorted(nums)` -> `(sorted_list, original_unchanged, None)`.

## Формат тестовых данных (`tests/07_list_mutation/NNN.in` -> `tests/07_list_mutation/NNN.out`)

Каждая строка: `evens n...` | `evens_buggy n...` | `grid_fixed R C` | `grid_buggy R C` (печатает сетку после присваивания `[0][0] = 1`) | `shallow_append X` | `deep_append X` | `sort n...` | `iadd`. Вывод - Python repr результата.
`main.py` предоставляет `solve(text) -> str`; `python3 src/07_list_mutation/main.py < tests/07_list_mutation/001.in` печатает ответ.

Запуск (из корня репозитория): `python3 -m unittest discover -s tests/07_list_mutation`
