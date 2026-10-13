"""List/dict/set comprehensions and generator expressions."""


def squares_of_evens(nums):
    return [n * n for n in nums if n % 2 == 0]


def flatten(nested):
    return [x for sub in nested for x in sub]  # read left-to-right like nested for-loops


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def word_lengths(words):
    return {w: len(w) for w in words}


def pairs_with_sum(nums, target):
    return [
        (nums[i], nums[j])
        for i in range(len(nums))
        for j in range(i + 1, len(nums))
        if nums[i] + nums[j] == target
    ]


def fizzbuzz(n):
    return [
        "FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i)
        for i in range(1, n + 1)
    ]


def invert(d):
    return {v: k for k, v in d.items()}


def unique_lengths(words):
    return {len(w) for w in words}


def sum_squares_lazy(n):
    """Generator expression: no intermediate list, O(1) memory."""
    return sum(i * i for i in range(n))


def loop_var_does_not_leak():
    """In Python 3 the comprehension variable lives in its own scope."""
    [x for x in range(3)]
    try:
        x  # noqa: F821
    except NameError:
        return True
    return False


def late_binding_bug():
    return [lambda: i for i in range(3)]  # all closures see the final i == 2


def late_binding_fixed():
    return [lambda i=i: i for i in range(3)]  # bind current value via default arg


def solve(text: str) -> str:
    """Lines: `fizzbuzz N` | `squares n...` | `lengths w...` | `pairs TARGET n...` | `transpose 1,2;3,4`."""
    out = []
    for line in text.splitlines():
        cmd, *args = line.split()
        if cmd == "fizzbuzz":
            res = fizzbuzz(int(args[0]))
        elif cmd == "squares":
            res = squares_of_evens(int(a) for a in args)
        elif cmd == "lengths":
            res = word_lengths(args)
        elif cmd == "pairs":
            res = pairs_with_sum([int(a) for a in args[1:]], int(args[0]))
        else:
            res = transpose([[int(c) for c in row.split(",")] for row in args[0].split(";")] if args else [])
        out.append(str(res))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
