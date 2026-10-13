# Протокол итератора

Реализуйте в `main.py`:

1. `Countdown(start)` - **итератор** в виде класса, выдающий `start, start-1, ..., 1`, а затем бросающий `StopIteration`. `iter(c) is c`.
2. `CountdownIterable(start)` - **итерируемый объект**, по которому можно проходить сколько угодно раз.
3. `fibonacci(n)` - ленивый генератор первых `n` чисел Фибоначчи.
4. `chunked(iterable, size)` - выдаёт списки по `size` элементов (последний может быть короче); должен работать с одноразовыми итераторами; `size < 1` -> `ValueError`.
5. `manual_for_loop(iterable)` - собирает элементы, используя только `iter()`, `next()` и `StopIteration` (то, что `for` делает «под капотом»).

## Формат тестовых данных (`tests/01_iterator_protocol/data/NNN.in` -> `tests/01_iterator_protocol/data/NNN.out`)

Каждая строка - одна команда: `fib N` | `countdown N` | `chunk SIZE item...`. Вывод - Python repr получившегося списка или имя класса исключения (например, `ValueError`).
`main.py` предоставляет `solve(text) -> str`; `python3 src/01_iterator_protocol/main.py < tests/01_iterator_protocol/data/001.in` печатает ответ.

Запуск (из корня репозитория): `python3 -m unittest discover -s tests/01_iterator_protocol`
