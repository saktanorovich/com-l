"""File handling and resource management: always release resources, even on errors."""
import contextlib
import os
import tempfile
from collections import Counter, deque


def count_lines(path) -> int:
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f)  # streams line by line, constant memory


def word_frequency(path) -> dict:
    counts = Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:
            counts.update(line.lower().split())
    return dict(counts)


def read_in_chunks(path, size: int = 8192):
    with open(path, encoding="utf-8") as f:
        while chunk := f.read(size):
            yield chunk


def atomic_write(path, content) -> None:
    """Write to a temp file in the same dir, then os.replace (atomic on POSIX/Windows)."""
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(str(content))
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.remove(tmp)
        raise


class ManagedFile:
    """Class-based context manager: __enter__ acquires, __exit__ always releases."""

    def __init__(self, path, mode="r"):
        self.path, self.mode = path, mode
        self.file = None

    def __enter__(self):
        self.file = open(self.path, self.mode, encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc, tb):
        self.file.close()
        return False  # do not swallow exceptions


@contextlib.contextmanager
def open_for_read(path):
    f = open(path, encoding="utf-8")
    try:
        yield f
    finally:
        f.close()


def tail(path, n: int) -> list:
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in deque(f, maxlen=n)]


def copy_file(src, dst) -> None:
    with open(src, encoding="utf-8") as r, open(dst, "w", encoding="utf-8") as w:
        for line in r:
            w.write(line)


def solve(text: str) -> str:
    """First line = command (`count` | `words` | `tail N` | `chunks N`); the rest is the file content."""
    command, _, content = text.partition("\n")
    name, *args = command.split()
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "input.txt")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        if name == "count":
            return f"{count_lines(path)}\n"
        if name == "words":
            return "".join(f"{w} {c}\n" for w, c in sorted(word_frequency(path).items()))
        if name == "tail":
            return "".join(line + "\n" for line in tail(path, int(args[0])))
        return f"{[len(c) for c in read_in_chunks(path, int(args[0]))]}\n"


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
