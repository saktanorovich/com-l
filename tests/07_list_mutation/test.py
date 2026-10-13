import importlib.util
import pathlib
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent

_spec = importlib.util.spec_from_file_location(
    "solution", pathlib.Path(__file__).resolve().parent.parent.parent / "src" / "07_list_mutation" / "main.py"
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


import copy


class TestShallowCopy(unittest.TestCase):
    def test_shallow_copy_shares_inner(self):
        a = [[1], [2]]
        b = m.shallow(a)
        b[0].append(99)
        self.assertEqual(a[0], [1, 99])
        self.assertIsNot(a, b)

    def test_shares_inner_report(self):
        self.assertTrue(m.shares_inner_objects([[1]], m.shallow([[1]])) is False)
        a = [[1]]
        self.assertTrue(m.shares_inner_objects(a, m.shallow(a)))

    def test_deep_copy_independent(self):
        a = [[1], [2]]
        b = m.deep(a)
        b[0].append(99)
        self.assertEqual(a[0], [1])

    def test_alias_is_same_object(self):
        a = [1]
        self.assertIs(m.alias(a), a)


class TestGridBug(unittest.TestCase):
    def test_buggy_grid_rows_shared(self):
        g = m.grid_buggy(2, 2)
        g[0][0] = 1
        self.assertEqual(g, [[1, 0], [1, 0]])

    def test_fixed_grid_independent(self):
        g = m.grid_fixed(2, 2)
        g[0][0] = 1
        self.assertEqual(g, [[1, 0], [0, 0]])


class TestMutableDefault(unittest.TestCase):
    def test_buggy_leaks_between_calls(self):
        m.append_buggy(1)
        self.assertEqual(m.append_buggy(2), [1, 2])

    def test_fixed_is_fresh(self):
        self.assertEqual(m.append_fixed(1), [1])
        self.assertEqual(m.append_fixed(2), [2])

    def test_fixed_uses_given_list(self):
        lst = [0]
        self.assertIs(m.append_fixed(1, lst), lst)


class TestMutateWhileIterating(unittest.TestCase):
    def test_buggy_skips_elements(self):
        self.assertEqual(m.remove_evens_buggy([2, 4, 6, 1]), [4, 1])

    def test_fixed_removes_all(self):
        data = [2, 4, 6, 1]
        self.assertEqual(m.remove_evens_fixed(data), [1])

    def test_fixed_inplace_keeps_identity(self):
        data = [2, 4, 1]
        out = m.remove_evens_inplace(data)
        self.assertIs(out, data)
        self.assertEqual(data, [1])


class TestOperators(unittest.TestCase):
    def test_iadd_mutates_add_does_not(self):
        self.assertEqual(m.iadd_vs_add(), (True, False))

    def test_sort_vs_sorted(self):
        self.assertEqual(m.sort_vs_sorted([3, 1, 2]), ([1, 2, 3], [3, 1, 2], None))

    def test_slice_copy_is_shallow(self):
        a = [[1]]
        self.assertIsNot(m.slice_copy(a), a)
        self.assertIs(m.slice_copy(a)[0], a[0])

class TestCopyEdges(unittest.TestCase):
    def test_empty_list(self):
        for f in (m.shallow, m.deep, m.slice_copy):
            a = []
            b = f(a)
            self.assertEqual(b, [])
            self.assertIsNot(b, a)

    def test_flat_list_shallow_is_independent(self):
        a = [1, 2]
        b = m.shallow(a)
        b.append(3)
        self.assertEqual(a, [1, 2])

    def test_shallow_reassigning_element_does_not_affect_original(self):
        a = [[1], [2]]
        b = m.shallow(a)
        b[0] = [9]
        self.assertEqual(a, [[1], [2]])

    def test_shares_inner_objects_edges(self):
        self.assertFalse(m.shares_inner_objects([], []))
        a = [[1], [2]]
        self.assertTrue(m.shares_inner_objects(a, m.shallow(a)))
        self.assertFalse(m.shares_inner_objects(a, m.deep(a)))

    def test_shallow_vs_slice_equivalent(self):
        a = [[1], 2]
        self.assertTrue(m.shares_inner_objects(a, m.slice_copy(a)))
        self.assertEqual(m.slice_copy(a), m.shallow(a))

    def test_deep_copy_handles_cycles(self):
        a = [1]
        a.append(a)
        b = m.deep(a)
        self.assertIsNot(b, a)
        self.assertIs(b[1], b)

    def test_deep_copy_preserves_internal_sharing(self):
        x = [1]
        a = [x, x]
        b = m.deep(a)
        self.assertIs(b[0], b[1])
        self.assertIsNot(b[0], x)

    def test_deep_copy_of_deeply_nested(self):
        a = [[[[1]]]]
        b = m.deep(a)
        b[0][0][0].append(2)
        self.assertEqual(a, [[[[1]]]])

    def test_deep_copy_with_tuple_and_dict_inside(self):
        a = [({"k": [1]},)]
        b = m.deep(a)
        b[0][0]["k"].append(2)
        self.assertEqual(a[0][0]["k"], [1])

    def test_alias_mutation_visible_both_ways(self):
        a = [1]
        b = m.alias(a)
        b.append(2)
        self.assertEqual(a, [1, 2])


class TestGridEdges(unittest.TestCase):
    def test_zero_rows_and_cols(self):
        self.assertEqual(m.grid_buggy(0, 3), [])
        self.assertEqual(m.grid_fixed(0, 3), [])
        self.assertEqual(m.grid_fixed(2, 0), [[], []])

    def test_buggy_rows_are_same_object(self):
        g = m.grid_buggy(3, 2)
        self.assertIs(g[0], g[2])

    def test_fixed_rows_are_distinct_objects(self):
        g = m.grid_fixed(3, 2)
        self.assertEqual(len({id(r) for r in g}), 3)

    def test_one_by_one(self):
        g = m.grid_fixed(1, 1)
        g[0][0] = 5
        self.assertEqual(g, [[5]])

    def test_shape(self):
        g = m.grid_fixed(4, 7)
        self.assertEqual((len(g), {len(r) for r in g}), (4, {7}))

    def test_buggy_row_replacement_is_fine(self):
        g = m.grid_buggy(2, 2)
        g[0] = [9, 9]  # rebinding a slot, not mutating the shared row
        self.assertEqual(g, [[9, 9], [0, 0]])


class TestDefaultArgEdges(unittest.TestCase):
    def test_buggy_default_object_is_shared(self):
        before = m.append_buggy.__defaults__[0]
        r = m.append_buggy("x")
        self.assertIs(r, m.append_buggy.__defaults__[0])
        self.assertIs(before, r)
        m.append_buggy.__defaults__[0].clear()

    def test_fixed_has_none_default(self):
        self.assertEqual(m.append_fixed.__defaults__, (None,))

    def test_fixed_respects_empty_list_argument(self):
        lst = []
        self.assertIs(m.append_fixed(1, lst), lst)
        self.assertEqual(lst, [1])

    def test_fixed_falsy_values_appended(self):
        self.assertEqual(m.append_fixed(0), [0])
        self.assertEqual(m.append_fixed(None), [None])

    def test_fixed_repeated_calls_independent_objects(self):
        self.assertIsNot(m.append_fixed(1), m.append_fixed(1))


class TestRemoveEvensEdges(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(m.remove_evens_fixed([]), [])
        self.assertEqual(m.remove_evens_buggy([]), [])
        data = []
        self.assertIs(m.remove_evens_inplace(data), data)
        self.assertEqual(data, [])

    def test_all_evens(self):
        self.assertEqual(m.remove_evens_fixed([2, 4, 6, 8]), [])
        self.assertEqual(m.remove_evens_inplace([2, 4, 6, 8]), [])

    def test_buggy_all_evens_leaves_survivors(self):
        self.assertEqual(m.remove_evens_buggy([2, 4, 6, 8]), [4, 8])

    def test_no_evens(self):
        self.assertEqual(m.remove_evens_fixed([1, 3]), [1, 3])

    def test_zero_and_negatives(self):
        self.assertEqual(m.remove_evens_fixed([-2, -1, 0, 1]), [-1, 1])

    def test_fixed_does_not_mutate_input(self):
        data = [1, 2, 3]
        out = m.remove_evens_fixed(data)
        self.assertEqual(data, [1, 2, 3])
        self.assertIsNot(out, data)

    def test_buggy_mutates_input(self):
        data = [2, 4]
        m.remove_evens_buggy(data)
        self.assertEqual(data, [4])

    def test_inplace_visible_through_alias(self):
        data = [1, 2, 3, 4]
        alias = data
        m.remove_evens_inplace(data)
        self.assertEqual(alias, [1, 3])

    def test_duplicates(self):
        self.assertEqual(m.remove_evens_fixed([2, 2, 2, 3, 3]), [3, 3])


class TestOperatorEdges(unittest.TestCase):
    def test_sort_vs_sorted_empty_and_single(self):
        self.assertEqual(m.sort_vs_sorted([]), ([], [], None))
        self.assertEqual(m.sort_vs_sorted([1]), ([1], [1], None))

    def test_sort_vs_sorted_duplicates_negatives(self):
        self.assertEqual(m.sort_vs_sorted([2, -1, 2]), ([-1, 2, 2], [2, -1, 2], None))

    def test_does_not_mutate_caller_list(self):
        nums = [3, 1, 2]
        m.sort_vs_sorted(nums)
        self.assertEqual(nums, [3, 1, 2])

    def test_already_sorted(self):
        self.assertEqual(m.sort_vs_sorted([1, 2, 3])[0], [1, 2, 3])

    def test_slice_copy_nested_shared_mutation(self):
        a = [[1]]
        b = m.slice_copy(a)
        b[0].append(2)
        self.assertEqual(a, [[1, 2]])

    def test_iadd_vs_add_repeatable(self):
        self.assertEqual(m.iadd_vs_add(), (True, False))
        self.assertEqual(m.iadd_vs_add(), (True, False))


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
