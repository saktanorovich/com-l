import importlib.util
import pathlib
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent
import contextlib

_spec = importlib.util.spec_from_file_location(
    "solution", pathlib.Path(__file__).resolve().parent.parent.parent / "src" / "05_file_handling" / "main.py"
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


import os
import tempfile


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def path(self, name):
        return os.path.join(self.dir, name)

    def write(self, name, text):
        with open(self.path(name), "w", encoding="utf-8", newline="") as f:
            f.write(text)
        return self.path(name)

    def read(self, name):
        with open(self.path(name), encoding="utf-8", newline="") as f:
            return f.read()


class TestCountEdges(Base):
    def test_empty_file(self):
        self.assertEqual(m.count_lines(self.write("a", "")), 0)

    def test_no_trailing_newline(self):
        self.assertEqual(m.count_lines(self.write("a", "a\nb")), 2)

    def test_only_newlines(self):
        self.assertEqual(m.count_lines(self.write("a", "\n\n\n")), 3)

    def test_single_line_no_newline(self):
        self.assertEqual(m.count_lines(self.write("a", "x")), 1)

    def test_windows_line_endings(self):
        self.assertEqual(m.count_lines(self.write("a", "a\r\nb\r\n")), 2)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            m.count_lines(self.path("nope"))

    def test_directory_instead_of_file(self):
        with self.assertRaises(OSError):
            m.count_lines(self.dir)

    def test_big_file(self):
        self.assertEqual(m.count_lines(self.write("a", "x\n" * 100000)), 100000)

    def test_invalid_utf8_raises(self):
        p = self.path("bin")
        with open(p, "wb") as f:
            f.write(b"\xff\xfe\xfa")
        with self.assertRaises(UnicodeDecodeError):
            m.count_lines(p)


class TestWordFrequencyEdges(Base):
    def test_empty_and_whitespace_only(self):
        self.assertEqual(m.word_frequency(self.write("a", "")), {})
        self.assertEqual(m.word_frequency(self.write("b", " \n\t \n")), {})

    def test_mixed_whitespace_and_case(self):
        self.assertEqual(m.word_frequency(self.write("a", "A\ta  a\nA")), {"a": 4})

    def test_unicode(self):
        self.assertEqual(m.word_frequency(self.write("a", "Ünï ünï")), {"ünï": 2})

    def test_punctuation_is_part_of_word(self):
        self.assertEqual(m.word_frequency(self.write("a", "hi hi,")), {"hi": 1, "hi,": 1})

    def test_missing(self):
        with self.assertRaises(FileNotFoundError):
            m.word_frequency(self.path("x"))


class TestChunkEdges(Base):
    def test_empty_file_no_chunks(self):
        self.assertEqual(list(m.read_in_chunks(self.write("a", ""), size=10)), [])

    def test_size_larger_than_file(self):
        self.assertEqual(list(m.read_in_chunks(self.write("a", "abc"), size=100)), ["abc"])

    def test_size_one(self):
        self.assertEqual(list(m.read_in_chunks(self.write("a", "abc"), size=1)), ["a", "b", "c"])

    def test_exact_multiple(self):
        self.assertEqual([len(c) for c in m.read_in_chunks(self.write("a", "x" * 6), size=3)], [3, 3])

    def test_multibyte_chars_not_split(self):
        text = "é" * 10
        self.assertEqual("".join(m.read_in_chunks(self.write("a", text), size=3)), text)

    def test_missing(self):
        with self.assertRaises(FileNotFoundError):
            list(m.read_in_chunks(self.path("x")))


class TestAtomicWriteEdges(Base):
    def test_creates_new_file(self):
        p = self.path("new")
        m.atomic_write(p, "x")
        self.assertEqual(self.read("new"), "x")

    def test_overwrites_longer_content(self):
        p = self.write("a", "long old content")
        m.atomic_write(p, "s")
        self.assertEqual(self.read("a"), "s")

    def test_empty_content(self):
        p = self.write("a", "old")
        m.atomic_write(p, "")
        self.assertEqual(self.read("a"), "")

    def test_unicode_content(self):
        p = self.path("a")
        m.atomic_write(p, "héllo ✓")
        self.assertEqual(self.read("a"), "héllo ✓")

    def test_non_string_content_is_stringified(self):
        m.atomic_write(self.path("a"), 123)
        self.assertEqual(self.read("a"), "123")

    def test_relative_path(self):
        cwd = os.getcwd()
        os.chdir(self.dir)
        self.addCleanup(os.chdir, cwd)
        m.atomic_write("rel.txt", "ok")
        self.assertEqual(self.read("rel.txt"), "ok")

    def test_missing_directory_raises_and_leaves_nothing(self):
        with self.assertRaises(OSError):
            m.atomic_write(os.path.join(self.dir, "no", "such", "f"), "x")
        self.assertEqual(os.listdir(self.dir), [])

    def test_no_temp_files_left_after_success(self):
        m.atomic_write(self.path("a"), "x")
        self.assertEqual(os.listdir(self.dir), ["a"])

    def test_failure_on_new_file_creates_nothing(self):
        class Boom:
            def __str__(self):
                raise RuntimeError
        with self.assertRaises(RuntimeError):
            m.atomic_write(self.path("a"), Boom())
        self.assertEqual(os.listdir(self.dir), [])


class TestContextManagerEdges(Base):
    def test_managed_file_missing_raises(self):
        with self.assertRaises(FileNotFoundError):
            with m.ManagedFile(self.path("nope")):
                pass

    def test_managed_file_does_not_swallow_exception_type(self):
        p = self.write("a", "x")
        with self.assertRaises(KeyError):
            with m.ManagedFile(p):
                raise KeyError

    def test_managed_file_write_mode(self):
        p = self.path("w")
        with m.ManagedFile(p, "w") as f:
            f.write("hi")
        self.assertEqual(self.read("w"), "hi")

    def test_managed_file_closed_after_normal_exit(self):
        p = self.write("a", "x")
        with m.ManagedFile(p) as f:
            pass
        self.assertTrue(f.closed)

    def test_open_for_read_closes_on_exception(self):
        p = self.write("a", "x")
        holder = {}
        with self.assertRaises(RuntimeError):
            with m.open_for_read(p) as f:
                holder["f"] = f
                raise RuntimeError
        self.assertTrue(holder["f"].closed)

    def test_open_for_read_missing(self):
        with self.assertRaises(FileNotFoundError):
            with m.open_for_read(self.path("nope")):
                pass

    def test_reusable_instance(self):
        p = self.write("a", "x")
        cm = m.ManagedFile(p)
        for _ in range(2):
            with cm as f:
                self.assertEqual(f.read(), "x")
            self.assertTrue(f.closed)


class TestTailEdges(Base):
    def test_n_larger_than_file(self):
        self.assertEqual(m.tail(self.write("a", "1\n2"), 10), ["1", "2"])

    def test_n_zero(self):
        self.assertEqual(m.tail(self.write("a", "1\n2"), 0), [])

    def test_empty_file(self):
        self.assertEqual(m.tail(self.write("a", ""), 3), [])

    def test_trailing_newline_not_extra_line(self):
        self.assertEqual(m.tail(self.write("a", "a\nb\n"), 1), ["b"])

    def test_blank_lines_kept(self):
        self.assertEqual(m.tail(self.write("a", "a\n\n\n"), 2), ["", ""])

    def test_negative_n(self):
        with self.assertRaises(ValueError):
            m.tail(self.write("a", "a"), -1)

    def test_missing(self):
        with self.assertRaises(FileNotFoundError):
            m.tail(self.path("x"), 1)


class TestCopyEdges(Base):
    def test_empty_source(self):
        src = self.write("s", "")
        m.copy_file(src, self.path("d"))
        self.assertEqual(self.read("d"), "")

    def test_overwrites_destination(self):
        src = self.write("s", "new")
        dst = self.write("d", "much older longer text")
        m.copy_file(src, dst)
        self.assertEqual(self.read("d"), "new")

    def test_missing_source_does_not_create_destination(self):
        with self.assertRaises(FileNotFoundError):
            m.copy_file(self.path("nope"), self.path("d"))
        self.assertFalse(os.path.exists(self.path("d")))

    def test_multiline_and_unicode(self):
        src = self.write("s", "a\nÿ\n\nlast")
        m.copy_file(src, self.path("d"))
        self.assertEqual(self.read("d"), "a\nÿ\n\nlast")

    def test_destination_in_missing_dir(self):
        src = self.write("s", "x")
        with self.assertRaises(FileNotFoundError):
            m.copy_file(src, os.path.join(self.dir, "no", "d"))

class TestCounting(Base):
    def test_count_lines(self):
        self.assertEqual(m.count_lines(self.write("a.txt", "a\nb\nc\n")), 3)

    def test_word_frequency(self):
        p = self.write("a.txt", "the cat The dog\nthe end")
        self.assertEqual(m.word_frequency(p), {"the": 3, "cat": 1, "dog": 1, "end": 1})

    def test_read_in_chunks_reassembles(self):
        p = self.write("a.txt", "x" * 1000)
        chunks = list(m.read_in_chunks(p, size=300))
        self.assertEqual([len(c) for c in chunks], [300, 300, 300, 100])


class TestSafeWrite(Base):
    def test_writes_content(self):
        p = self.path("out.txt")
        m.atomic_write(p, "hello")
        with open(p, encoding="utf-8") as f:
            self.assertEqual(f.read(), "hello")

    def test_failure_keeps_old_file_and_cleans_temp(self):
        p = self.write("out.txt", "old")

        class Boom:
            def __str__(self):
                raise RuntimeError

        with self.assertRaises(Exception):
            m.atomic_write(p, Boom())
        with open(p, encoding="utf-8") as f:
            self.assertEqual(f.read(), "old")
        self.assertEqual(os.listdir(self.dir), ["out.txt"])


class TestContextManagers(Base):
    def test_class_based_manager_closes_on_error(self):
        p = self.write("a.txt", "x")
        holder = {}
        with self.assertRaises(ValueError):
            with m.ManagedFile(p) as f:
                holder["f"] = f
                raise ValueError
        self.assertTrue(holder["f"].closed)

    def test_generator_manager_closes(self):
        p = self.write("a.txt", "x")
        with m.open_for_read(p) as f:
            self.assertEqual(f.read(), "x")
        self.assertTrue(f.closed)

    def test_tail(self):
        p = self.write("a.txt", "\n".join(str(i) for i in range(10)))
        self.assertEqual(m.tail(p, 3), ["7", "8", "9"])

    def test_copy_file_with_two_resources(self):
        src = self.write("s.txt", "data")
        dst = self.path("d.txt")
        m.copy_file(src, dst)
        with open(dst, encoding="utf-8") as f:
            self.assertEqual(f.read(), "data")


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
