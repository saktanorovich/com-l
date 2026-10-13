# Списковые включения (List Comprehension)

Реализуйте каждую функцию в `main.py` одним включением / генераторным выражением:

1. `squares_of_evens(nums)`
2. `flatten(nested)` (один уровень)
3. `transpose(matrix)`
4. `word_lengths(words)` (словарное включение)
5. `pairs_with_sum(nums, target)` - пары `i < j` с заданной суммой
6. `fizzbuzz(n)` - список строк для 1..n
7. `invert(d)`, `unique_lengths(words)` (множественное включение)
8. `sum_squares_lazy(n)` - сумма `i*i` для `i in range(n)` без промежуточного списка
9. `loop_var_does_not_leak()` - доказать область видимости включения
10. `late_binding_bug()` / `late_binding_fixed()` - замыкания внутри включения

## Формат тестовых данных (`tests/04_list_comprehension/NNN.in` -> `tests/04_list_comprehension/NNN.out`)

Каждая строка: `fizzbuzz N` | `squares n...` | `lengths word...` | `pairs TARGET n...` | `transpose 1,2;3,4`. Вывод - Python repr результата.
`main.py` предоставляет `solve(text) -> str`; `python3 src/04_list_comprehension/main.py < tests/04_list_comprehension/001.in` печатает ответ.

Запуск (из корня репозитория): `python3 -m unittest discover -s tests/04_list_comprehension`
