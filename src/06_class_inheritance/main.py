"""Class inheritance: super(), MRO, ABCs, mixins, class vs instance attributes."""
import json
import math
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    def describe(self) -> str:
        return "Shape"


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2


class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h

    def describe(self):
        return super().describe() + " Rectangle"


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def describe(self):
        return super().describe() + " Square"


def total_area(shapes) -> float:
    return sum(s.area() for s in shapes)  # polymorphism


# Diamond: D -> B, C -> A. C3 linearization gives D, B, C, A, object.
class A:
    def hello(self):
        return ["A"]


class B(A):
    def hello(self):
        return ["B"] + super().hello()


class C(A):
    def hello(self):
        return ["C"] + super().hello()


class D(B, C):
    def hello(self):
        return ["D"] + super().hello()


def diamond_mro() -> list:
    return [k.__name__ for k in D.__mro__]


class JsonMixin:
    def to_json(self) -> str:
        return json.dumps(vars(self))


class Point(JsonMixin):
    def __init__(self, x, y):
        self.x, self.y = x, y


class Counter:
    created = 0  # class attribute: shared

    def __init__(self):
        self.n = 0  # instance attribute: per object
        Counter.created += 1

    def bump(self):
        self.n += 1


class Animal:
    registry: dict = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Animal.registry[cls.__name__] = cls

    def speak(self):
        raise NotImplementedError


class Dog(Animal):
    def speak(self):
        return "Woof"


class Cat(Animal):
    def speak(self):
        return "Meow"


def solve(text: str) -> str:
    """Lines: `area rect W H|square S|circle R|shape` | `describe ...` | `mro X` | `hello X` | `speak animal`."""
    kinds = {"rect": Rectangle, "square": Square, "circle": Circle, "shape": Shape}
    out = []
    for line in text.splitlines():
        cmd, *args = line.split()
        try:
            if cmd in ("area", "describe"):
                obj = kinds[args[0]](*[int(a) for a in args[1:]])
                res = obj.area() if cmd == "area" else obj.describe()
            elif cmd == "mro":
                res = " ".join(k.__name__ for k in globals()[args[0]].__mro__)
            elif cmd == "hello":
                res = " ".join(globals()[args[0]]().hello())
            else:
                res = Animal.registry[args[0].capitalize()]().speak()
        except Exception as e:
            res = type(e).__name__
        out.append(str(res))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
