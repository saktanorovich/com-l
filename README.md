# Python Problems

A repository for solving Python problems. Each topic lives in its own folder under `src/` with a task statement in English and Russian (`task-en.md`, `task-ru.md`), a solution (`main.py`), and tests under `tests/`.

## Topics

| # | Topic | Folder |
|---|---|---|
| 1 | Iterator protocol | `src/01_iterator_protocol` |
| 2 | Decorators | `src/02_decorators` |
| 3 | Threading and the GIL | `src/03_threading_gil` |
| 4 | List comprehension | `src/04_list_comprehension` |
| 5 | File handling and resource management | `src/05_file_handling` |
| 6 | Class inheritance | `src/06_class_inheritance` |
| 7 | List mutation (shallow copy) | `src/07_list_mutation` |

## Running

```bash
# one topic
python3 -m unittest discover -s tests/01_iterator_protocol

# all topics
for d in tests/*/; do python3 -m unittest discover -s "$d"; done
```

## Notes

Interview Q&A for these topics: `docs/ANSWERS.en.md` (English), `docs/ANSWERS.ru.md` (Russian).
