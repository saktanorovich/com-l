# Потоки и GIL

Реализуйте в `main.py`:

1. `SafeCounter` - потокобезопасный счётчик (`increment()`, `.value`) на основе `Lock`; `run_counter(counter, threads, increments)` запускает его из многих потоков и возвращает итоговое значение.
2. `parallel_map_io(func, items, workers)` - map на потоках для I/O-задач; сохраняет порядок входных данных, пробрасывает исключения.
3. `parallel_map_cpu(func, items, workers)` - то же для CPU-задач, в обход GIL через процессы.
4. `producer_consumer(items, consumers)` - конвейер на `queue.Queue`; каждый потребитель удваивает элементы; остановка через «сентинелы».
5. `why_increment_is_not_atomic()` - вернуть байт-код `dis` для `x += 1` над глобальной переменной, чтобы показать, почему GIL не заменяет блокировки.

Граничные правила: `producer_consumer(items, consumers)` при `consumers < 1` бросает `ValueError` (потребителей останавливает приватный сентинел, а не `None`); `sum_of_squares(n)` - вспомогательная CPU-функция (`sum(i*i for i in range(n))`, `0` при `n <= 0`).

## Формат тестовых данных (`tests/03_threading_gil/NNN.in` -> `tests/03_threading_gil/NNN.out`)

Каждая строка: `counter THREADS N` | `mapio WORKERS x...` (квадраты) | `cpu n...` (`sum_of_squares`) | `pipe CONSUMERS x...` (отсортированные удвоенные значения). Вывод - результат или имя класса исключения.
`main.py` предоставляет `solve(text) -> str`; `python3 src/03_threading_gil/main.py < tests/03_threading_gil/001.in` печатает ответ.

Запуск (из корня репозитория): `python3 -m unittest discover -s tests/03_threading_gil`
