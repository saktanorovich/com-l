import importlib.util
import pathlib
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent
_MAIN = _ROOT.parent.parent / "src" / "01_iterator_protocol" / "main.py"


class _Lazy:
    """Loads the implementation on first attribute access so each test fails on its own."""

    _mod = None

    def __getattr__(self, name):
        if _Lazy._mod is None:
            spec = importlib.util.spec_from_file_location("iterator_protocol_main", _MAIN)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _Lazy._mod = mod
        return getattr(_Lazy._mod, name)


m = _Lazy()


class TestCountdown(unittest.TestCase):
    def test_counts_down_to_one(self):
        self.assertEqual(list(m.Countdown(3)), [3, 2, 1])

    def test_zero_is_empty(self):
        self.assertEqual(list(m.Countdown(0)), [])

    def test_is_its_own_iterator(self):
        c = m.Countdown(2)
        self.assertIs(iter(c), c)

    def test_exhausted_raises_stop_iteration(self):
        c = m.Countdown(1)
        next(c)
        with self.assertRaises(StopIteration):
            next(c)


class TestCountdownIterable(unittest.TestCase):
    def test_can_be_iterated_many_times(self):
        c = m.CountdownIterable(3)
        self.assertEqual(list(c), [3, 2, 1])
        self.assertEqual(list(c), [3, 2, 1])


class TestFibonacci(unittest.TestCase):
    def test_first_values(self):
        self.assertEqual(list(m.fibonacci(6)), [0, 1, 1, 2, 3, 5])

    def test_is_lazy_generator(self):
        import inspect
        self.assertTrue(inspect.isgenerator(m.fibonacci(5)))

    def test_zero(self):
        self.assertEqual(list(m.fibonacci(0)), [])


class TestChunked(unittest.TestCase):
    def test_even_split(self):
        self.assertEqual(list(m.chunked([1, 2, 3, 4], 2)), [[1, 2], [3, 4]])

    def test_last_chunk_shorter(self):
        self.assertEqual(list(m.chunked(range(5), 2)), [[0, 1], [2, 3], [4]])

    def test_works_on_one_shot_iterators(self):
        self.assertEqual(list(m.chunked(iter("abcde"), 3)), [["a", "b", "c"], ["d", "e"]])

    def test_invalid_size(self):
        with self.assertRaises(ValueError):
            list(m.chunked([1], 0))


class TestManualFor(unittest.TestCase):
    def test_matches_builtin_for(self):
        self.assertEqual(m.manual_for_loop(iter([1, 2, 3])), [1, 2, 3])

    def test_empty(self):
        self.assertEqual(m.manual_for_loop([]), [])

class TestCountdownEdges(unittest.TestCase):
    def test_negative_start_is_empty(self):
        self.assertEqual(list(m.Countdown(-5)), [])

    def test_single_element(self):
        self.assertEqual(list(m.Countdown(1)), [1])

    def test_stays_exhausted(self):
        c = m.Countdown(1)
        list(c)
        for _ in range(3):
            with self.assertRaises(StopIteration):
                next(c)

    def test_iterator_is_single_use(self):
        c = m.Countdown(2)
        self.assertEqual(list(c), [2, 1])
        self.assertEqual(list(c), [])

    def test_iterable_independent_iterators(self):
        it = m.CountdownIterable(3)
        a, b = iter(it), iter(it)
        self.assertEqual(next(a), 3)
        self.assertEqual(next(a), 2)
        self.assertEqual(next(b), 3)  # b unaffected by a

    def test_iterable_zero_and_negative(self):
        self.assertEqual(list(m.CountdownIterable(0)), [])
        self.assertEqual(list(m.CountdownIterable(-1)), [])


class TestFibonacciEdges(unittest.TestCase):
    def test_one_and_two(self):
        self.assertEqual(list(m.fibonacci(1)), [0])
        self.assertEqual(list(m.fibonacci(2)), [0, 1])

    def test_negative_is_empty(self):
        self.assertEqual(list(m.fibonacci(-3)), [])

    def test_large_values_are_exact(self):
        self.assertEqual(list(m.fibonacci(100))[-1], 218922995834555169026)

    def test_lazy_does_not_compute_ahead(self):
        g = m.fibonacci(10 ** 12)  # would never finish if eager
        self.assertEqual([next(g) for _ in range(5)], [0, 1, 1, 2, 3])


class TestChunkedEdges(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(list(m.chunked([], 3)), [])

    def test_size_larger_than_input(self):
        self.assertEqual(list(m.chunked([1, 2], 10)), [[1, 2]])

    def test_size_one(self):
        self.assertEqual(list(m.chunked("abc", 1)), [["a"], ["b"], ["c"]])

    def test_size_equals_length(self):
        self.assertEqual(list(m.chunked([1, 2, 3], 3)), [[1, 2, 3]])

    def test_negative_size(self):
        with self.assertRaises(ValueError):
            list(m.chunked([1], -1))

    def test_falsy_items_are_kept(self):
        self.assertEqual(list(m.chunked([0, None, "", False], 2)), [[0, None], ["", False]])

    def test_accepts_generator_and_stays_lazy(self):
        def gen():
            yield from range(3)
            raise AssertionError("consumed too far")

        it = m.chunked(gen(), 3)
        self.assertEqual(next(it), [0, 1, 2])  # must not pull past the first chunk

    def test_infinite_source(self):
        import itertools
        it = m.chunked(itertools.count(), 2)
        self.assertEqual([next(it), next(it)], [[0, 1], [2, 3]])


class TestManualForEdges(unittest.TestCase):
    def test_string_dict_generator(self):
        self.assertEqual(m.manual_for_loop("ab"), ["a", "b"])
        self.assertEqual(m.manual_for_loop({"k": 1}), ["k"])
        self.assertEqual(m.manual_for_loop(x for x in range(3)), [0, 1, 2])

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.manual_for_loop(42)

    def test_exhausted_iterator_gives_empty(self):
        it = iter([1])
        list(it)
        self.assertEqual(m.manual_for_loop(it), [])

    def test_matches_builtin_for_none_items(self):
        self.assertEqual(m.manual_for_loop([None, 0]), [None, 0])


class TestSolveFormat(unittest.TestCase):
    def test_output_ends_with_newline(self):
        self.assertEqual(m.solve("fib 3\n"), "[0, 1, 1]\n")

    def test_one_line_per_input_line(self):
        self.assertEqual(m.solve("countdown 2\nfib 2\n"), "[2, 1]\n[0, 1]\n")

    def test_chunk_items_stay_strings(self):
        self.assertEqual(m.solve("chunk 2 1 2 3\n"), "[['1', '2'], ['3']]\n")

    def test_exception_name_on_error(self):
        self.assertEqual(m.solve("chunk 0 a b\n"), "ValueError\n")


class TestChunkedLazyError(unittest.TestCase):
    def test_value_error_only_when_advanced(self):
        g = m.chunked([1], 0)  # no error at call time
        with self.assertRaises(ValueError):
            next(g)


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
