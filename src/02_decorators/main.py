"""Decorators: a callable that takes a function and returns a (usually wrapped) function."""
import functools
import time


def call_counter(func):
    @functools.wraps(func)  # keep __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def retry(times: int, exceptions: tuple = (Exception,)):
    """Decorator factory (3 levels): retry(...) -> decorator -> wrapper."""
    if times < 1:
        raise ValueError("times must be >= 1")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise

        return wrapper

    return decorator


def memoize(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last_duration = time.perf_counter() - start

    wrapper.last_duration = None
    return wrapper


def stacking_order() -> list:
    """Decorators apply bottom-up, but the outermost wrapper runs first at call time."""
    order = []

    def tag(name):
        def deco(fn):
            @functools.wraps(fn)
            def wrapper(*a, **k):
                order.append(name)
                return fn(*a, **k)

            return wrapper

        return deco

    @tag("outer")
    @tag("inner")
    def f():
        pass

    f()
    return order


def solve(text: str) -> str:
    """Lines: `fib N` -> "value computations" | `retry TIMES FAILS` -> "ok attempts" / "ValueError attempts"."""
    out = []
    for line in text.splitlines():
        cmd, *args = line.split()
        if cmd == "fib":
            computed = []

            @memoize
            def fib(n):
                computed.append(n)
                return n if n < 2 else fib(n - 1) + fib(n - 2)

            out.append(f"{fib(int(args[0]))} {len(computed)}")
        else:
            times, fails = int(args[0]), int(args[1])
            try:
                decorator = retry(times, (ValueError,))
            except ValueError:
                out.append("ValueError")
                continue
            attempts = []

            @decorator
            def flaky():
                attempts.append(1)
                if len(attempts) <= fails:
                    raise ValueError
                return "ok"

            try:
                result = flaky()
            except ValueError:
                result = "ValueError"
            out.append(f"{result} {len(attempts)}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
