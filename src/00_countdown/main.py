"""Countdown: a class-based iterator (__iter__ returns self, __next__ raises StopIteration when done)."""


class Countdown:
    """An iterator that is its own iterator - single use."""

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


def solve(text: str) -> str:
    """stdin/stdout driver. Each line: `countdown N`."""
    out = [str(list(Countdown(int(line.split()[1])))) for line in text.splitlines()]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
