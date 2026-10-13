import pathlib
import sys
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent
import threading

# import as a real module (not via spec) so ProcessPoolExecutor children can unpickle functions
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent / "src" / "03_threading_gil"))
import main as m  # noqa: E402

import time


class TestSafeCounter(unittest.TestCase):
    def test_no_lost_updates(self):
        self.assertEqual(m.run_counter(m.SafeCounter(), threads=8, increments=20000), 160000)

    def test_value_property(self):
        c = m.SafeCounter()
        c.increment(); c.increment()
        self.assertEqual(c.value, 2)


class TestParallelIO(unittest.TestCase):
    def test_preserves_order(self):
        def slow(x):
            time.sleep(0.05 * (3 - x))
            return x * 10
        self.assertEqual(m.parallel_map_io(slow, [0, 1, 2], workers=3), [0, 10, 20])

    def test_actually_concurrent(self):
        start = time.perf_counter()
        m.parallel_map_io(lambda _: time.sleep(0.2), range(5), workers=5)
        self.assertLess(time.perf_counter() - start, 0.6)

    def test_propagates_exceptions(self):
        def boom(x):
            raise RuntimeError("bad")
        with self.assertRaises(RuntimeError):
            m.parallel_map_io(boom, [1], workers=1)


class TestParallelCPU(unittest.TestCase):
    def test_results_match_serial(self):
        nums = [10, 100, 1000, 5000]
        self.assertEqual(
            m.parallel_map_cpu(m.sum_of_squares, nums, workers=2),
            [m.sum_of_squares(n) for n in nums],
        )


class TestProducerConsumer(unittest.TestCase):
    def test_all_items_processed_once(self):
        self.assertEqual(sorted(m.producer_consumer(range(50), consumers=4)), [x * 2 for x in range(50)])


class TestRace(unittest.TestCase):
    def test_unsafe_read_modify_write_is_not_atomic_pattern(self):
        # explanation helper: documents why `+=` needs a lock
        self.assertIn("LOAD", m.why_increment_is_not_atomic())

class TestCounterEdges(unittest.TestCase):
    def test_zero_threads(self):
        self.assertEqual(m.run_counter(m.SafeCounter(), threads=0, increments=10), 0)

    def test_zero_increments(self):
        self.assertEqual(m.run_counter(m.SafeCounter(), threads=4, increments=0), 0)

    def test_single_thread(self):
        self.assertEqual(m.run_counter(m.SafeCounter(), threads=1, increments=100), 100)

    def test_starts_at_zero(self):
        self.assertEqual(m.SafeCounter().value, 0)

    def test_independent_instances(self):
        a, b = m.SafeCounter(), m.SafeCounter()
        a.increment()
        self.assertEqual((a.value, b.value), (1, 0))

    def test_many_threads_few_increments(self):
        self.assertEqual(m.run_counter(m.SafeCounter(), threads=50, increments=3), 150)

    def test_no_threads_leak(self):
        before = threading.active_count()
        m.run_counter(m.SafeCounter(), threads=5, increments=10)
        self.assertEqual(threading.active_count(), before)


class TestParallelIOEdges(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(m.parallel_map_io(str, [], workers=4), [])

    def test_single_worker_is_serial_but_correct(self):
        self.assertEqual(m.parallel_map_io(lambda x: x + 1, [1, 2, 3], workers=1), [2, 3, 4])

    def test_more_items_than_workers(self):
        self.assertEqual(m.parallel_map_io(lambda x: x * x, range(100), workers=3), [x * x for x in range(100)])

    def test_accepts_generator(self):
        self.assertEqual(m.parallel_map_io(lambda x: x, (i for i in range(5)), workers=2), [0, 1, 2, 3, 4])

    def test_invalid_workers(self):
        with self.assertRaises(ValueError):
            m.parallel_map_io(lambda x: x, [1], workers=0)

    def test_duplicates_and_none_results(self):
        self.assertEqual(m.parallel_map_io(lambda x: None, [1, 1, 1], workers=2), [None, None, None])

    def test_one_failure_among_many_raises(self):
        def f(x):
            if x == 3:
                raise KeyError("three")
            return x
        with self.assertRaises(KeyError):
            m.parallel_map_io(f, range(6), workers=3)

    def test_slow_first_item_does_not_reorder(self):
        def f(x):
            time.sleep(0.1 if x == 0 else 0)
            return x
        self.assertEqual(m.parallel_map_io(f, range(5), workers=5), [0, 1, 2, 3, 4])


class TestParallelCPUEdges(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(m.parallel_map_cpu(m.sum_of_squares, [], workers=2), [])

    def test_sum_of_squares_small_values(self):
        self.assertEqual([m.sum_of_squares(n) for n in (0, 1, 2, 3)], [0, 0, 1, 5])

    def test_negative_input(self):
        self.assertEqual(m.sum_of_squares(-5), 0)

    def test_single_item_single_worker(self):
        self.assertEqual(m.parallel_map_cpu(m.sum_of_squares, [4], workers=1), [14])

    def test_worker_exception_propagates(self):
        with self.assertRaises(TypeError):
            m.parallel_map_cpu(m.sum_of_squares, ["x"], workers=1)


class TestProducerConsumerEdges(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(m.producer_consumer([], consumers=3), [])

    def test_more_consumers_than_items(self):
        self.assertEqual(sorted(m.producer_consumer([1, 2], consumers=10)), [2, 4])

    def test_single_consumer_preserves_order(self):
        self.assertEqual(m.producer_consumer([3, 1, 2], consumers=1), [6, 2, 4])

    def test_duplicates_preserved(self):
        self.assertEqual(m.producer_consumer([1, 1, 1], consumers=2), [2, 2, 2])

    def test_zero_and_negative_items(self):
        self.assertEqual(sorted(m.producer_consumer([0, -1], consumers=2)), [-2, 0])

    def test_invalid_consumers(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                m.producer_consumer([1], consumers=bad)

    def test_generator_input(self):
        self.assertEqual(sorted(m.producer_consumer((i for i in range(10)), consumers=3)), [i * 2 for i in range(10)])


class TestBytecode(unittest.TestCase):
    def test_shows_load_and_store(self):
        text = m.why_increment_is_not_atomic()
        self.assertIn("LOAD", text)
        self.assertIn("STORE", text)


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
