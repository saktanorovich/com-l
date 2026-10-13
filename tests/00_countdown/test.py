import importlib.util
import pathlib
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent
_MAIN = _ROOT.parent.parent / "src" / "00_countdown" / "main.py"


class _Lazy:
    """Loads the implementation on first attribute access so each test fails on its own."""

    _mod = None

    def __getattr__(self, name):
        if _Lazy._mod is None:
            spec = importlib.util.spec_from_file_location("countdown_iterator_main", _MAIN)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _Lazy._mod = mod
        return getattr(_Lazy._mod, name)


m = _Lazy()


class TestYieldsStartDownToOne(unittest.TestCase):
    def test_counts_down_to_one(self):
        self.assertEqual(list(m.Countdown(3)), [3, 2, 1])

    def test_single_element(self):
        self.assertEqual(list(m.Countdown(1)), [1])

    def test_raises_stop_iteration_after_last_value(self):
        c = m.Countdown(1)
        self.assertEqual(next(c), 1)
        with self.assertRaises(StopIteration):
            next(c)


class TestStaysExhausted(unittest.TestCase):
    def test_keeps_raising_stop_iteration(self):
        c = m.Countdown(2)
        list(c)
        for _ in range(3):
            with self.assertRaises(StopIteration):
                next(c)


class TestNonPositiveStart(unittest.TestCase):
    def test_zero_is_empty(self):
        self.assertEqual(list(m.Countdown(0)), [])

    def test_negative_is_empty(self):
        self.assertEqual(list(m.Countdown(-5)), [])


class TestIterReturnsSelf(unittest.TestCase):
    def test_iter_is_identity(self):
        c = m.Countdown(2)
        self.assertIs(iter(c), c)


class TestSinglePass(unittest.TestCase):
    def test_second_pass_yields_nothing(self):
        c = m.Countdown(2)
        self.assertEqual(list(c), [2, 1])
        self.assertEqual(list(c), [])


class TestSolve(unittest.TestCase):
    def test_output_ends_with_newline(self):
        self.assertEqual(m.solve("countdown 2\n"), "[2, 1]\n")

    def test_one_output_line_per_input_line(self):
        self.assertEqual(m.solve("countdown 2\ncountdown 0\n"), "[2, 1]\n[]\n")


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
