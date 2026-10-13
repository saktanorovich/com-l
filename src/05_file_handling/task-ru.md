# Работа с файлами и управление ресурсами

Реализуйте в `main.py`:

1. `count_lines(path)` и `word_frequency(path)` (без учёта регистра) - потоковая обработка, не загружайте файл целиком.
2. `read_in_chunks(path, size)` - генератор блоков.
3. `atomic_write(path, content)` - временный файл + `os.replace`; при ошибке старый файл остаётся нетронутым, временного файла не остаётся.
4. `ManagedFile` - менеджер контекста в виде класса (`__enter__`/`__exit__`), закрывает файл даже при исключениях.
5. `open_for_read(path)` - то же через `@contextlib.contextmanager`.
6. `tail(path, n)` - последние `n` строк при постоянном расходе памяти.
7. `copy_file(src, dst)` - два ресурса в одном `with`.

## Формат тестовых данных (`tests/05_file_handling/NNN.in` -> `tests/05_file_handling/NNN.out`)

Первая строка - команда (`count` | `words` | `tail N` | `chunks N`); остальной ввод - содержимое файла, с которым нужно работать. `words` печатает строки `слово количество`, отсортированные по слову; `tail` печатает строки; `chunks` печатает список длин блоков.
`main.py` предоставляет `solve(text) -> str`; `python3 src/05_file_handling/main.py < tests/05_file_handling/001.in` печатает ответ.

Запуск (из корня репозитория): `python3 -m unittest discover -s tests/05_file_handling`
