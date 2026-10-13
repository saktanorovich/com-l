# Декораторы

Реализуйте в `main.py`:

1. `call_counter` - предоставляет `.calls`; должен сохранять `__name__`/`__doc__` (`functools.wraps`).
2. `retry(times, exceptions)` - **фабрика** декораторов; повторяет вызов только при указанных исключениях, после последней попытки пробрасывает исключение дальше.
3. `memoize` - кэш по позиционным и именованным аргументам.
4. `timed` - сохраняет время последнего запуска в `.last_duration`, даже если функция бросила исключение.
5. `stacking_order()` - показать, что при `@outer @inner` первой срабатывает обёртка `outer`. Вернуть `["outer", "inner"]`.

Граничное правило: `retry(times, ...)` при `times < 1` бросает `ValueError`.

## Формат тестовых данных (`tests/02_decorators/NNN.in` -> `tests/02_decorators/NNN.out`)

Каждая строка: `fib N` печатает `<значение> <число реальных вычислений>`; `retry TIMES FAILS` запускает функцию, которая падает `FAILS` раз с `ValueError`, и печатает `ok <попытки>` или `ValueError <попытки>` (просто `ValueError`, если `TIMES < 1`).
`main.py` предоставляет `solve(text) -> str`; `python3 src/02_decorators/main.py < tests/02_decorators/001.in` печатает ответ.

Запуск (из корня репозитория): `python3 -m unittest discover -s tests/02_decorators`
