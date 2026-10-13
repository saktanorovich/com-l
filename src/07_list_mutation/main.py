"""List mutation, aliasing and shallow vs deep copy."""
import copy


def alias(a):
    return a  # same object, not a copy


def shallow(a):
    return copy.copy(a)  # new outer list, SAME inner objects


def deep(a):
    return copy.deepcopy(a)


def shares_inner_objects(a, b) -> bool:
    return any(x is y for x, y in zip(a, b))


def slice_copy(a):
    return a[:]  # also shallow


def grid_buggy(rows, cols):
    return [[0] * cols] * rows  # `rows` references to ONE row


def grid_fixed(rows, cols):
    return [[0] * cols for _ in range(rows)]


def append_buggy(x, lst=[]):  # default evaluated once at def time
    lst.append(x)
    return lst


def append_fixed(x, lst=None):
    if lst is None:
        lst = []
    lst.append(x)
    return lst


def remove_evens_buggy(nums):
    for n in nums:  # deleting shifts indices -> skips the next element
        if n % 2 == 0:
            nums.remove(n)
    return nums


def remove_evens_fixed(nums):
    return [n for n in nums if n % 2]


def remove_evens_inplace(nums):
    nums[:] = [n for n in nums if n % 2]  # slice assignment keeps identity
    return nums


def iadd_vs_add():
    a = [1]
    b = a
    a += [2]  # in-place extend
    mutated = a is b
    a = a + [3]  # new list
    return mutated, a is b


def sort_vs_sorted(nums):
    original = list(nums)
    out = sorted(original)  # returns new list, original untouched
    probe = list(nums)
    ret = probe.sort()  # in-place, returns None
    return out, original, ret


def solve(text: str) -> str:
    """Lines: `evens n...` | `evens_buggy n...` | `grid_fixed R C` | `grid_buggy R C` (set [0][0]=1)
    | `shallow_append X` | `deep_append X` | `sort n...` | `iadd`."""
    out = []
    for line in text.splitlines():
        cmd, *args = line.split()
        nums = [int(a) for a in args]
        if cmd == "evens":
            res = remove_evens_fixed(nums)
        elif cmd == "evens_buggy":
            res = remove_evens_buggy(nums)
        elif cmd in ("grid_fixed", "grid_buggy"):
            res = (grid_fixed if cmd == "grid_fixed" else grid_buggy)(*nums)
            if res and res[0]:
                res[0][0] = 1
        elif cmd in ("shallow_append", "deep_append"):
            original = [[1], [2]]
            (shallow if cmd == "shallow_append" else deep)(original)[0].append(nums[0])
            res = original
        elif cmd == "sort":
            res = sort_vs_sorted(nums)
        else:
            res = iadd_vs_add()
        out.append(str(res))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
