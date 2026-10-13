# Summary: Project Requirements

## Project Overview
- **Client:** a large US bank (global enterprise). Security requirements restrict the available infrastructure.
- **Product:** a Python layer on top of the client's existing AI models, using the client's LLMs. It is a system for validating and developing financial models, with process automation where possible.
- **Scale:** a large, long-term project that has not been worked on before. The team is new and separate, with up to 8 members.

## Project Requirements
1. **No existing infrastructure.** The team designs it, including architecture and processes.
2. **Automation** of model validation and development processes.
3. **Documentation and testing.** Validating models in a global enterprise requires extensive documentation and testing.
4. **Security constraints.** The client's security requirements limit the infrastructure that can be used.
5. **Client engagement.** The client's manager is based in London and is closely involved in the project. The manager expects an engaged team and regular interaction.

## Stack and Environment
Linux, Python, PyCharm, AWS-code (as written in the source; exact service not specified), GitHub Copilot, the client's LLMs.

## Technical Topics (Python)
Iterator Protocol; decorators; threading and the GIL; list comprehension; file handling and resource management; class inheritance; list mutation (shallow copy).

## Open Questions
- The exact meaning of "AWS-code" (for example CodeCommit, CodeBuild or another service).
- Project duration, work format and time zone are not specified.

---

# Python Reference

## 1. Iterator Protocol
An *iterable* implements `__iter__()`, which returns an *iterator*. An *iterator* implements `__next__()`, which returns the next item or raises `StopIteration` when exhausted, and `__iter__()`, which returns the iterator itself. A `for` loop calls `iter(obj)` and then calls `next()` repeatedly until `StopIteration` is raised.
```python
class Countdown:
    def __init__(self, n): self.n = n
    def __iter__(self): return self
    def __next__(self):
        if self.n <= 0: raise StopIteration
        self.n -= 1
        return self.n + 1

list(Countdown(3))  # [3, 2, 1]
```
- Generator functions (`yield`) construct iterators automatically; they are lazy and use constant memory.
- An iterator is single-use. An iterable such as `list` produces a new iterator on each `iter()` call.
- `iter(callable, sentinel)` calls the callable until it returns the sentinel. `next(it, default)` returns `default` instead of raising `StopIteration`.

## 2. Decorators
A decorator is a callable that accepts a function and returns a replacement function, usually a wrapper. `@dec` is equivalent to `f = dec(f)`. Decorators rely on functions being first-class objects and on closures capturing enclosing variables.
```python
import functools, time

def timed(func):
    @functools.wraps(func)          # preserves __name__, __doc__
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__}: {time.perf_counter() - start:.4f}s")
    return wrapper

def retry(times):                    # decorator with arguments: three nested levels
    def deco(func):
        @functools.wraps(func)
        def wrapper(*a, **kw):
            for i in range(times):
                try: return func(*a, **kw)
                except Exception:
                    if i == times - 1: raise
        return wrapper
    return deco
```
- `functools.wraps` preserves the wrapped function's metadata.
- Stacked decorators are applied bottom-up; the outermost wrapper runs first at call time.
- Typical uses: logging, timing, caching (`functools.lru_cache`), authorization, retries, validation.
- A class implementing `__call__` can also serve as a decorator.

## 3. Threading and the GIL
In CPython, the Global Interpreter Lock (GIL) allows one thread to execute Python bytecode at a time. Threads therefore do not provide CPU parallelism for pure-Python code, but they do provide concurrency for I/O-bound work because the GIL is released during blocking I/O.
- I/O-bound work: `threading`, `ThreadPoolExecutor`, or `asyncio`.
- CPU-bound work: `multiprocessing` or `ProcessPoolExecutor` (separate processes, each with its own GIL), or C extensions such as NumPy that release the GIL.
- The GIL does not make compound operations thread-safe. `x += 1` is not atomic; use `threading.Lock` or `queue.Queue`.
- Related topics: race conditions, deadlocks (lock ordering), daemon threads, `join()`.
- CPython 3.13 introduced an experimental free-threaded build without the GIL.
```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(8) as pool:
    results = list(pool.map(fetch, urls))
```

## 4. List Comprehension
Syntax for building a list from an iterable: `[expr for x in iterable if cond]`. It is generally shorter and faster than an equivalent loop with `append`.
```python
squares = [x**2 for x in range(10) if x % 2 == 0]
flat    = [y for row in matrix for y in row]               # nested: outer loop first
labels  = ["even" if x % 2 == 0 else "odd" for x in nums]  # conditional expression precedes `for`
```
- Variants: set `{x for ...}`, dict `{k: v for ...}`, generator expression `(x for ...)` (lazy; no list is built).
- In Python 3 the loop variable is local to the comprehension and does not leak into the enclosing scope.
- Deeply nested comprehensions reduce readability; a generator expression avoids materializing large results.

## 5. File Handling and Resource Management
The `with` statement uses a context manager (`__enter__` / `__exit__`) to release a resource even when an exception occurs.
```python
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:            # lazy, line-by-line iteration
        process(line)
```
- Modes: `r`, `w` (truncates), `a`, `x`, `b` (binary), `+`. Specify `encoding` explicitly for text files.
- Without `with`, use `try/finally` and call `f.close()`.
- Custom context managers: a class with `__enter__` / `__exit__`, or a generator decorated with `@contextlib.contextmanager`.
- Multiple resources: `with open(a) as f, open(b) as g:`; `contextlib.ExitStack` for a dynamic number.
- `pathlib.Path` provides `.read_text()` and `.write_text()`. The same principle applies to database connections, locks and sockets.
```python
from contextlib import contextmanager

@contextmanager
def managed(resource):
    try:
        yield resource
    finally:
        resource.close()
```

## 6. Class Inheritance
A subclass reuses and extends the behavior of a parent class (`class Child(Parent)`). Python supports multiple inheritance; attribute lookup follows the method resolution order (MRO, C3 linearization), available as `Class.__mro__`.
```python
class Animal:
    def __init__(self, name): self.name = name
    def speak(self): raise NotImplementedError

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)      # call the parent initializer
        self.breed = breed
    def speak(self): return "Woof"  # method overriding
```
- `super()` follows the MRO, which is required for cooperative multiple inheritance (diamond hierarchies).
- `isinstance` and `issubclass` test class relationships. Abstract base classes use `abc.ABC` and `@abstractmethod`.
- Composition is preferred when the relationship is not "is-a"; mixins provide small reusable behaviors.
- If a subclass overrides `__init__` without calling `super().__init__()`, the parent's state is not initialized.

## 7. List Mutation (Shallow Copy)
Lists are mutable, and assignment copies the reference rather than the data. A shallow copy creates a new outer list whose elements are the same objects as in the original, so nested mutable objects are shared.
```python
a = [1, 2, 3]
b = a            # same object: b.append(4) also changes a
c = a.copy()     # also a[:], list(a), copy.copy(a): new outer list

nested = [[1, 2], [3, 4]]
sh = nested.copy()
sh[0].append(99)
print(nested)    # [[1, 2, 99], [3, 4]]  (inner list is shared)

import copy
deep = copy.deepcopy(nested)   # fully independent copy
```
- Identity can be checked with `is` and `id()`.
- `[[0]*3]*3` creates three references to one row. Use `[[0]*3 for _ in range(3)]`.
- A mutable default argument (`def f(x, acc=[])`) is created once and shared across calls. Use `None` and create the list inside the function.
- Removing items from a list while iterating over it skips elements. Iterate over a copy or build a new list.
