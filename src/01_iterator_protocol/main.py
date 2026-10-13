"""Iterator protocol: __iter__ returns an iterator, __next__ returns items or raises StopIteration."""
from collections.abc import Iterable, Iterator


class Countdown:
    """An iterator (is its own iterator) - single use."""

    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


class CountdownIterable:
    """An iterable: every iter() call returns a fresh iterator, so it is reusable."""

    def __init__(self, start: int):
        self.start = start

    def __iter__(self):
        return Countdown(self.start)


def fibonacci(n: int):
    """Generator: yields the first n Fibonacci numbers lazily."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def chunked(iterable: Iterable, size: int):
    """Yield lists of at most `size` items; works on one-shot iterators."""
    if size < 1:
        raise ValueError("size must be >= 1")
    it = iter(iterable)
    while chunk := list(_take(it, size)):
        yield chunk


def _take(it: Iterator, n: int):
    for _ in range(n):
        try:
            yield next(it)
        except StopIteration:
            return


def manual_for_loop(iterable: Iterable) -> list:
    """What `for x in iterable` does under the hood."""
    result = []
    it = iter(iterable)
    while True:
        try:
            item = next(it)
        except StopIteration:
            break
        result.append(item)
    return result


def solve(text: str) -> str:
    """stdin/stdout driver. Lines: `fib N` | `countdown N` | `chunk SIZE item...`."""
    out = []
    for line in text.splitlines():
        cmd, *args = line.split()
        try:
            if cmd == "fib":
                res = list(fibonacci(int(args[0])))
            elif cmd == "countdown":
                res = list(Countdown(int(args[0])))
            else:
                res = list(chunked(args[1:], int(args[0])))
        except Exception as e:
            res = type(e).__name__
        out.append(str(res))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
