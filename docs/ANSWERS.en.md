# Interview Answers (Python)

Project context: Python / Linux / LLM-based validation tooling for a bank. Expect questions on correctness, resource safety and concurrency. Each topic has a runnable folder with a task, tests and a solution (`NN_topic/{task-en.md, task-ru.md, main.py, tests/}`); run everything with `./run_all.sh`.

---

## 1. Iterator Protocol  (`01_iterator_protocol`)

**Q: What is the difference between an iterable and an iterator?**
An *iterable* has `__iter__()` returning an iterator (list, str, dict, file). An *iterator* has `__next__()` (returns the next item or raises `StopIteration`) and `__iter__()` returning itself. Iterators are single-use; iterables can be re-iterated.

**Q: What does `for x in obj` do?**
Calls `iter(obj)`, then repeatedly `next(it)` until `StopIteration` (see `manual_for_loop`).

**Q: Generator vs iterator class?**
A generator function (with `yield`) builds an iterator automatically; state lives in the suspended frame. Lazy, O(1) memory, much shorter than a class. Use a class when you need extra methods/state (e.g. `peek`, `reset`).

**Q: Why is returning `self` from `__iter__` a gotcha?**
Second loop over the same object is empty (exhausted). Return a new iterator in `__iter__` for re-usable collections (`CountdownIterable`).

**Q: `iter(callable, sentinel)`?** Calls callable until it returns sentinel, e.g. `iter(lambda: f.read(1024), "")`.

Also: `yield from`, `itertools` (`islice`, `chain`, `tee`), generators can't be rewound, `StopIteration` inside a generator becomes `RuntimeError` (PEP 479).

---

## 2. Decorators  (`02_decorators`)

**Q: What is a decorator?**
A callable taking a function and returning a replacement; `@d def f` is `f = d(f)`. Used for cross-cutting concerns: logging, timing, retry, caching, auth.

**Q: Why `functools.wraps`?**
Without it the wrapper hides `__name__`, `__doc__`, annotations, `__wrapped__` - breaking debugging, introspection and docs.

**Q: How do decorators with arguments work?**
Three layers: `retry(3)` returns the real decorator, which returns the wrapper (`retry` in `main.py`).

**Q: Order of stacked decorators?**
Applied bottom-up (`@a @b def f` = `a(b(f))`); at call time the outermost wrapper runs first.

**Q: Class-based decorators?** Implement `__call__`; useful for state. Decorating methods needs `__get__` or use function decorators.

**Q: Pitfalls?** Forgetting `return`, not forwarding `*args, **kwargs`, mutable shared state in cache (unbounded growth - prefer `functools.lru_cache(maxsize=...)`), unhashable args in memoization.

---

## 3. Threading and the GIL  (`03_threading_gil`)

**Q: What is the GIL?**
A mutex in CPython so only one thread runs Python bytecode at a time. It protects interpreter internals (refcounts, memory management).

**Q: Consequences?**
- CPU-bound code gets no speedup from threads -> use `multiprocessing` / `ProcessPoolExecutor`, NumPy/C extensions that release the GIL, or other runtimes.
- I/O-bound code (network, disk, `sleep`) does benefit: the GIL is released while blocking -> `ThreadPoolExecutor`, or `asyncio` for many connections.

**Q: Does the GIL make my code thread-safe?**
No. `counter += 1` is load/add/store; the interpreter may switch threads between them (lost updates). Use `threading.Lock`, `queue.Queue`, or avoid shared state. Compound operations are never safe by default.

**Q: Threads vs processes vs asyncio?**
Threads: shared memory, cheap, I/O-bound. Processes: separate memory + GIL each, CPU-bound, pay pickling/IPC cost. asyncio: single thread, cooperative, best for thousands of I/O waits; blocking calls stall the loop.

**Q: Other tools?** `RLock` (re-entrant), `Semaphore`, `Event`, `Condition`, deadlocks (consistent lock ordering, timeouts), daemon threads, `join()`.

**Q: Anything new?** Python 3.13+ ships an *experimental free-threaded* build (PEP 703, no GIL) - not default; library support is still maturing. For an enterprise bank, assume the GIL exists.

For LLM workloads: API calls are I/O-bound -> threads/asyncio with rate limiting and retries; post-processing/number crunching -> processes.

---

## 4. List Comprehension  (`04_list_comprehension`)

**Q: Syntax?** `[expr for x in it if cond]`; dict `{k: v for ...}`, set `{e for ...}`, generator `(e for ...)`.

**Q: Why use them?** More readable and usually faster than `append` loops (no repeated method lookup, optimized bytecode).

**Q: Nested comprehension order?** Same as nested loops written left to right: `[x for sub in nested for x in sub]`.

**Q: List comprehension vs generator expression?** List builds everything in memory; generator is lazy/O(1) memory and single-use. Use a generator when feeding `sum`, `any`, `max`, etc.

**Q: Scope?** Loop variable doesn't leak in Python 3. But closures capture variables, not values: `[lambda: i for i in range(3)]` all return 2 -> fix with `lambda i=i: i`.

**Q: When NOT to use?** Side effects, deep nesting, multiple conditions that hurt readability, very long expressions - use a normal loop.

**Q: Conditional expression vs filter?** `[a if c else b for x in it]` (transform) vs `[x for x in it if c]` (filter) - position of `if` matters.

---

## 5. File Handling and Resource Management  (`05_file_handling`)

**Q: Why use `with open(...)`?**
Guarantees `close()` (flush + release descriptor) even on exceptions. Relying on GC/`close()` manually leaks descriptors and may lose buffered data.

**Q: How do context managers work?**
`__enter__` acquires and returns the resource; `__exit__(exc_type, exc, tb)` releases; return truthy to suppress the exception. Or use `@contextlib.contextmanager` with `try/finally` around `yield`. `ExitStack` for dynamic numbers of resources.

**Q: How to read big files?**
Iterate the file object (line by line) or `read(size)` in chunks; never `read()`/`readlines()` a multi-GB file.

**Q: Text vs binary mode, encoding?**
Always pass `encoding="utf-8"` explicitly for text (default is locale-dependent); use `"rb"/"wb"` for bytes. `newline` handling is translated in text mode.

**Q: How to write a file safely?**
Write a temp file in the same directory, `flush` + `os.fsync` (if durability matters), then `os.replace` (atomic) - readers never see a half-written file (`atomic_write`).

**Q: Other points:** `pathlib.Path` over string paths, `tempfile`, `shutil`, modes `r/w/a/x/+`, `FileNotFoundError`/`PermissionError` handling, file locking for concurrent writers, `open` flush buffering.

---

## 6. Class Inheritance  (`06_class_inheritance`)

**Q: How does `super()` work?**
It returns a proxy that delegates to the **next class in the MRO**, not necessarily the direct parent. Cooperative multiple inheritance requires every class to call `super()`.

**Q: What is the MRO?**
Method Resolution Order, computed with C3 linearization; inspect with `Cls.__mro__`. Diamond `D(B, C)` -> `D, B, C, A, object`; `A` is called once.

**Q: Abstract classes?**
`abc.ABC` + `@abstractmethod`: subclass can't be instantiated until all abstract methods are overridden.

**Q: Inheritance vs composition?**
Prefer composition ("has-a") for flexibility; inheritance ("is-a") for true subtyping (Liskov). Mixins add small reusable behavior (`JsonMixin`).

**Q: Class vs instance attributes?**
Class attributes are shared by all instances (and are mutable-trap if lists/dicts); `self.x = ...` creates an instance attribute that shadows the class one.

**Q: Other:** `isinstance`/`issubclass`, overriding vs extending (call `super().method()`), `__init_subclass__` for registries/plugins, name mangling (`__x`), `@classmethod` / `@staticmethod`, `@property`, duck typing / `Protocol`, `dataclass`.

---

## 7. List Mutation (Shallow Copy)  (`07_list_mutation`)

**Q: `b = a` vs `a.copy()` vs `deepcopy`?**
`b = a` - same object (alias). `a.copy()`, `a[:]`, `list(a)`, `copy.copy(a)` - new outer list, but **same inner objects** (shallow). `copy.deepcopy(a)` - recursively copies everything.

**Q: Classic example?**
`a = [[1], [2]]; b = a.copy(); b[0].append(9)` -> `a` is `[[1, 9], [2]]` too.

**Q: `[[0]*3]*3` bug?**
Creates 3 references to one row; changing one cell changes all rows. Use `[[0]*3 for _ in range(3)]`.

**Q: Mutable default arguments?**
`def f(x, lst=[])` - the default is created once at definition time and shared between calls. Use `None` sentinel.

**Q: Modifying a list while iterating?**
Removal shifts indices and skips elements. Build a new list (comprehension), iterate over a copy, or `nums[:] = [...]` to mutate in place and keep identity (important when others hold a reference).

**Q: `+=` vs `+`?**
`a += [x]` mutates in place (`extend`) and affects aliases; `a = a + [x]` creates a new list.

**Q: `sort()` vs `sorted()`?** `sort()` in-place returns `None`; `sorted()` returns a new list. Classic bug: `x = x.sort()`.

**Q: Immutable tuple containing a list?** The tuple can't change, but the inner list still can (`t[0].append(1)`) - and `t[0] += [1]` raises `TypeError` *after* mutating.

**Q: Function arguments?** Python passes object references: mutating a list argument inside a function is visible to the caller; rebinding the parameter is not.
