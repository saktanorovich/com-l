import importlib.util
import pathlib
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent

_spec = importlib.util.spec_from_file_location(
    "solution", pathlib.Path(__file__).resolve().parent.parent.parent / "src" / "02_decorators" / "main.py"
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


class TestCallCounter(unittest.TestCase):
    def test_counts_calls(self):
        @m.call_counter
        def f():
            return 1
        f(); f(); f()
        self.assertEqual(f.calls, 3)

    def test_keeps_metadata(self):
        @m.call_counter
        def f():
            """doc"""
        self.assertEqual(f.__name__, "f")
        self.assertEqual(f.__doc__, "doc")


class TestRetry(unittest.TestCase):
    def test_succeeds_after_failures(self):
        state = {"n": 0}

        @m.retry(times=3, exceptions=(ValueError,))
        def flaky():
            state["n"] += 1
            if state["n"] < 3:
                raise ValueError
            return "ok"

        self.assertEqual(flaky(), "ok")
        self.assertEqual(state["n"], 3)

    def test_raises_after_exhausting(self):
        state = {"n": 0}

        @m.retry(times=2, exceptions=(ValueError,))
        def bad():
            state["n"] += 1
            raise ValueError("x")

        with self.assertRaises(ValueError):
            bad()
        self.assertEqual(state["n"], 2)

    def test_other_exceptions_not_retried(self):
        state = {"n": 0}

        @m.retry(times=5, exceptions=(ValueError,))
        def bad():
            state["n"] += 1
            raise KeyError

        with self.assertRaises(KeyError):
            bad()
        self.assertEqual(state["n"], 1)


class TestMemoize(unittest.TestCase):
    def test_caches(self):
        calls = []

        @m.memoize
        def sq(x):
            calls.append(x)
            return x * x

        self.assertEqual(sq(4), 16)
        self.assertEqual(sq(4), 16)
        self.assertEqual(calls, [4])

    def test_distinguishes_args(self):
        @m.memoize
        def add(a, b=0):
            return a + b
        self.assertEqual(add(1, b=2), 3)
        self.assertEqual(add(1, b=3), 4)


class TestTimer(unittest.TestCase):
    def test_records_duration(self):
        @m.timed
        def f():
            return 5
        self.assertEqual(f(), 5)
        self.assertGreaterEqual(f.last_duration, 0)


class TestStacking(unittest.TestCase):
    def test_order_of_application(self):
        order = []

        def tag(name):
            def deco(fn):
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
        self.assertEqual(order, ["outer", "inner"])
        self.assertEqual(m.stacking_order(), ["outer", "inner"])

class TestCallCounterEdges(unittest.TestCase):
    def test_zero_before_any_call(self):
        @m.call_counter
        def f():
            pass
        self.assertEqual(f.calls, 0)

    def test_forwards_args_kwargs_and_return(self):
        @m.call_counter
        def f(a, b=2, *rest, **kw):
            return (a, b, rest, kw)
        self.assertEqual(f(1, 3, 4, z=5), (1, 3, (4,), {"z": 5}))

    def test_counts_calls_that_raise(self):
        @m.call_counter
        def f():
            raise ValueError
        for _ in range(2):
            with self.assertRaises(ValueError):
                f()
        self.assertEqual(f.calls, 2)

    def test_counters_are_independent(self):
        @m.call_counter
        def f():
            pass

        @m.call_counter
        def g():
            pass
        f(); f(); g()
        self.assertEqual((f.calls, g.calls), (2, 1))

    def test_wrapped_attribute(self):
        def f():
            pass
        self.assertIs(m.call_counter(f).__wrapped__, f)


class TestRetryEdges(unittest.TestCase):
    def test_times_one_means_no_retry(self):
        n = {"c": 0}

        @m.retry(times=1)
        def f():
            n["c"] += 1
            raise ValueError
        with self.assertRaises(ValueError):
            f()
        self.assertEqual(n["c"], 1)

    def test_invalid_times(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                m.retry(times=bad)

    def test_success_first_try_called_once(self):
        n = {"c": 0}

        @m.retry(times=5)
        def f():
            n["c"] += 1
            return 1
        self.assertEqual(f(), 1)
        self.assertEqual(n["c"], 1)

    def test_returns_falsy_values_without_retry(self):
        n = {"c": 0}

        @m.retry(times=3)
        def f():
            n["c"] += 1
            return None
        self.assertIsNone(f())
        self.assertEqual(n["c"], 1)

    def test_multiple_exception_types_and_subclass(self):
        n = {"c": 0}

        @m.retry(times=3, exceptions=(KeyError, OSError))
        def f():
            n["c"] += 1
            if n["c"] == 1:
                raise FileNotFoundError  # subclass of OSError
            if n["c"] == 2:
                raise KeyError
            return "ok"
        self.assertEqual(f(), "ok")

    def test_reraises_the_last_exception(self):
        n = {"c": 0}

        @m.retry(times=3)
        def f():
            n["c"] += 1
            raise ValueError(f"attempt {n['c']}")
        with self.assertRaisesRegex(ValueError, "attempt 3"):
            f()

    def test_forwards_arguments_and_metadata(self):
        @m.retry(times=2)
        def add(a, b=0):
            """doc"""
            return a + b
        self.assertEqual(add(1, b=2), 3)
        self.assertEqual((add.__name__, add.__doc__), ("add", "doc"))


class TestMemoizeEdges(unittest.TestCase):
    def test_none_result_is_cached(self):
        calls = []

        @m.memoize
        def f(x):
            calls.append(x)
        f(1); f(1)
        self.assertEqual(calls, [1])

    def test_kwarg_order_irrelevant(self):
        calls = []

        @m.memoize
        def f(a=0, b=0):
            calls.append(1)
            return a + b
        f(a=1, b=2); f(b=2, a=1)
        self.assertEqual(len(calls), 1)

    def test_exceptions_are_not_cached(self):
        calls = []

        @m.memoize
        def f(x):
            calls.append(x)
            raise ValueError
        for _ in range(2):
            with self.assertRaises(ValueError):
                f(1)
        self.assertEqual(len(calls), 2)

    def test_unhashable_argument(self):
        @m.memoize
        def f(x):
            return 1
        with self.assertRaises(TypeError):
            f([1])

    def test_separate_caches_per_function(self):
        @m.memoize
        def f(x):
            return "f"

        @m.memoize
        def g(x):
            return "g"
        self.assertEqual((f(1), g(1)), ("f", "g"))

    def test_no_args(self):
        n = []

        @m.memoize
        def f():
            n.append(1)
            return 7
        self.assertEqual((f(), f()), (7, 7))
        self.assertEqual(len(n), 1)

    def test_recursive_memoized_fib_is_fast(self):
        @m.memoize
        def fib(n):
            return n if n < 2 else fib(n - 1) + fib(n - 2)
        self.assertEqual(fib(90), 2880067194370816120)


class TestTimedEdges(unittest.TestCase):
    def test_none_before_first_call(self):
        @m.timed
        def f():
            pass
        self.assertIsNone(f.last_duration)

    def test_set_even_if_function_raises(self):
        @m.timed
        def f():
            raise RuntimeError
        with self.assertRaises(RuntimeError):
            f()
        self.assertIsNotNone(f.last_duration)

    def test_measures_sleep(self):
        import time

        @m.timed
        def f():
            time.sleep(0.05)
        f()
        self.assertGreaterEqual(f.last_duration, 0.04)

    def test_forwards_args(self):
        @m.timed
        def f(a, b=1):
            return a * b
        self.assertEqual(f(2, b=3), 6)


class TestFileCases(unittest.TestCase):
    """Data-driven cases: NNN.in -> m.solve(text) must equal NNN.out (one test per case)."""

    def test_has_40_cases(self):
        self.assertEqual(len(list(_ROOT.glob("*.in"))), 40)


def _make_case_test(inp):
    def test(self):
        out = inp.with_suffix(".out")
        self.assertTrue(out.exists(), f"missing {out.name}")
        self.assertEqual(
            m.solve(inp.read_text(encoding="utf-8")).rstrip("\n"),
            out.read_text(encoding="utf-8").rstrip("\n"),
        )
    return test


for _inp in sorted(_ROOT.glob("*.in")):
    setattr(TestFileCases, f"test_case_{_inp.stem}", _make_case_test(_inp))


if __name__ == "__main__":
    unittest.main()
