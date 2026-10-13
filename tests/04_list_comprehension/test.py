import importlib.util
import pathlib
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent

_spec = importlib.util.spec_from_file_location(
    "solution", pathlib.Path(__file__).resolve().parent.parent.parent / "src" / "04_list_comprehension" / "main.py"
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


class TestComprehensions(unittest.TestCase):
    def test_squares_of_evens(self):
        self.assertEqual(m.squares_of_evens(range(7)), [0, 4, 16, 36])

    def test_flatten(self):
        self.assertEqual(m.flatten([[1, 2], [3], [], [4, 5]]), [1, 2, 3, 4, 5])

    def test_transpose(self):
        self.assertEqual(m.transpose([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]])

    def test_word_lengths(self):
        self.assertEqual(m.word_lengths(["a", "abc"]), {"a": 1, "abc": 3})

    def test_pairs_with_sum(self):
        self.assertEqual(m.pairs_with_sum([1, 2, 3, 4], 5), [(1, 4), (2, 3)])

    def test_fizzbuzz(self):
        self.assertEqual(m.fizzbuzz(5), ["1", "2", "Fizz", "4", "Buzz"])
        self.assertEqual(m.fizzbuzz(15)[-1], "FizzBuzz")

    def test_invert_dict(self):
        self.assertEqual(m.invert({"a": 1, "b": 2}), {1: "a", 2: "b"})

    def test_unique_sorted_set_comp(self):
        self.assertEqual(m.unique_lengths(["a", "bb", "cc", "d"]), {1, 2})

    def test_lazy_sum_of_squares_generator(self):
        self.assertEqual(m.sum_squares_lazy(4), 14)

    def test_comprehension_variable_does_not_leak(self):
        self.assertTrue(m.loop_var_does_not_leak())

    def test_late_binding_lambdas(self):
        self.assertEqual([f() for f in m.late_binding_bug()], [2, 2, 2])
        self.assertEqual([f() for f in m.late_binding_fixed()], [0, 1, 2])

class TestEdges(unittest.TestCase):
    def test_squares_of_evens_empty_negative_zero(self):
        self.assertEqual(m.squares_of_evens([]), [])
        self.assertEqual(m.squares_of_evens([-4, -3, 0]), [16, 0])
        self.assertEqual(m.squares_of_evens([1, 3, 5]), [])

    def test_squares_accepts_generator(self):
        self.assertEqual(m.squares_of_evens(x for x in range(5)), [0, 4, 16])

    def test_flatten_empty_cases(self):
        self.assertEqual(m.flatten([]), [])
        self.assertEqual(m.flatten([[], []]), [])
        self.assertEqual(m.flatten([[1]]), [1])

    def test_flatten_one_level_only(self):
        self.assertEqual(m.flatten([[1, [2]], [3]]), [1, [2], 3])

    def test_flatten_does_not_mutate_input(self):
        data = [[1], [2]]
        m.flatten(data)
        self.assertEqual(data, [[1], [2]])

    def test_transpose_empty_and_degenerate(self):
        self.assertEqual(m.transpose([]), [])
        self.assertEqual(m.transpose([[]]), [])
        self.assertEqual(m.transpose([[1, 2, 3]]), [[1], [2], [3]])
        self.assertEqual(m.transpose([[1], [2], [3]]), [[1, 2, 3]])

    def test_transpose_ragged_truncates_to_shortest(self):
        self.assertEqual(m.transpose([[1, 2], [3]]), [[1, 3]])

    def test_transpose_twice_is_identity(self):
        a = [[1, 2], [3, 4], [5, 6]]
        self.assertEqual(m.transpose(m.transpose(a)), a)

    def test_transpose_returns_lists_not_tuples(self):
        self.assertTrue(all(isinstance(r, list) for r in m.transpose([[1, 2]])))

    def test_word_lengths_edge(self):
        self.assertEqual(m.word_lengths([]), {})
        self.assertEqual(m.word_lengths(["", "a", "a"]), {"": 0, "a": 1})
        self.assertEqual(m.word_lengths(["héllo"]), {"héllo": 5})

    def test_pairs_with_sum_edges(self):
        self.assertEqual(m.pairs_with_sum([], 1), [])
        self.assertEqual(m.pairs_with_sum([5], 10), [])  # no pairing with itself
        self.assertEqual(m.pairs_with_sum([1, 2], 100), [])
        self.assertEqual(m.pairs_with_sum([2, 2, 2], 4), [(2, 2)] * 3)
        self.assertEqual(m.pairs_with_sum([-1, 1, 0], 0), [(-1, 1)])
        self.assertEqual(m.pairs_with_sum([0, 0], 0), [(0, 0)])

    def test_fizzbuzz_edges(self):
        self.assertEqual(m.fizzbuzz(0), [])
        self.assertEqual(m.fizzbuzz(-3), [])
        self.assertEqual(m.fizzbuzz(1), ["1"])
        r = m.fizzbuzz(30)
        self.assertEqual((r[2], r[4], r[14], r[29]), ("Fizz", "Buzz", "FizzBuzz", "FizzBuzz"))
        self.assertEqual(len(r), 30)

    def test_invert_edges(self):
        self.assertEqual(m.invert({}), {})
        self.assertEqual(m.invert({"a": 1, "b": 1}), {1: "b"})  # last wins
        self.assertEqual(m.invert(m.invert({"a": 1})), {"a": 1})

    def test_invert_unhashable_values(self):
        with self.assertRaises(TypeError):
            m.invert({"a": [1]})

    def test_unique_lengths_edges(self):
        self.assertEqual(m.unique_lengths([]), set())
        self.assertEqual(m.unique_lengths(["", ""]), {0})

    def test_sum_squares_lazy_edges(self):
        self.assertEqual(m.sum_squares_lazy(0), 0)
        self.assertEqual(m.sum_squares_lazy(1), 0)
        self.assertEqual(m.sum_squares_lazy(-5), 0)
        self.assertEqual(m.sum_squares_lazy(10 ** 6), sum(i * i for i in range(10 ** 6)))

    def test_late_binding_edges(self):
        self.assertEqual(len(m.late_binding_bug()), 3)
        self.assertEqual([f() for f in m.late_binding_fixed()], [0, 1, 2])
        self.assertEqual([f() for f in m.late_binding_fixed()], [0, 1, 2])  # repeatable


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
