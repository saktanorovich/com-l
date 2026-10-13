"""Threading and the GIL.

The GIL lets only one thread execute Python bytecode at a time (in the default CPython build).
=> threads help for I/O-bound work (GIL released while waiting), NOT for CPU-bound work
   (use multiprocessing / ProcessPoolExecutor, or native code that releases the GIL).
The GIL does NOT make `counter += 1` atomic: use a Lock.
"""
import dis
import queue
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


class SafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    @property
    def value(self):
        return self._value


def run_counter(counter, threads: int, increments: int) -> int:
    def work():
        for _ in range(increments):
            counter.increment()

    pool = [threading.Thread(target=work) for _ in range(threads)]
    for t in pool:
        t.start()
    for t in pool:
        t.join()
    return counter.value


def parallel_map_io(func, items, workers: int = 8) -> list:
    """Threaded map for I/O-bound work; result order == input order; exceptions propagate."""
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(func, items))


def sum_of_squares(n: int) -> int:
    return sum(i * i for i in range(n))


def parallel_map_cpu(func, items, workers: int = 2) -> list:
    """Process pool sidesteps the GIL for CPU-bound work (func must be picklable/top-level)."""
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(func, items))


def producer_consumer(items, consumers: int = 4) -> list:
    """Queue-based pipeline: queue.Queue is thread-safe. Sentinel (None) stops each consumer."""
    if consumers < 1:
        raise ValueError("consumers must be >= 1")
    stop = object()  # private sentinel: cannot collide with a real item such as None
    tasks, results = queue.Queue(), queue.Queue()

    def consume():
        while (item := tasks.get()) is not stop:
            results.put(item * 2)

    workers = [threading.Thread(target=consume) for _ in range(consumers)]
    for w in workers:
        w.start()
    for item in items:
        tasks.put(item)
    for _ in workers:
        tasks.put(stop)
    for w in workers:
        w.join()
    return [results.get() for _ in range(results.qsize())]


_shared = 0


def _unsafe_increment():
    global _shared
    _shared += 1


def why_increment_is_not_atomic() -> str:
    """`x += 1` compiles to LOAD, add, STORE: a thread switch between them loses updates."""
    import io

    buf = io.StringIO()
    dis.dis(_unsafe_increment, file=buf)
    return buf.getvalue()


def solve(text: str) -> str:
    """Lines: `counter THREADS N` | `mapio WORKERS x...` (squares) | `cpu n...` | `pipe CONSUMERS x...`."""
    out = []
    for line in text.splitlines():
        cmd, *args = line.split()
        nums = [int(a) for a in args]
        try:
            if cmd == "counter":
                res = run_counter(SafeCounter(), nums[0], nums[1])
            elif cmd == "mapio":
                res = parallel_map_io(lambda x: x * x, nums[1:], workers=nums[0])
            elif cmd == "cpu":
                res = parallel_map_cpu(sum_of_squares, nums, workers=2)
            else:
                res = sorted(producer_consumer(nums[1:], consumers=nums[0]))
        except Exception as e:
            res = type(e).__name__
        out.append(str(res))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
