import importlib.util
import pathlib
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent
import json
import math

_spec = importlib.util.spec_from_file_location(
    "solution", pathlib.Path(__file__).resolve().parent.parent.parent / "src" / "06_class_inheritance" / "main.py"
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


class TestShapes(unittest.TestCase):
    def test_shape_is_abstract(self):
        with self.assertRaises(TypeError):
            m.Shape()

    def test_areas(self):
        self.assertAlmostEqual(m.Circle(1).area(), 3.14159265, places=5)
        self.assertEqual(m.Rectangle(2, 3).area(), 6)

    def test_square_is_rectangle_using_super(self):
        s = m.Square(4)
        self.assertIsInstance(s, m.Rectangle)
        self.assertEqual(s.area(), 16)
        self.assertEqual((s.w, s.h), (4, 4))

    def test_polymorphic_total(self):
        self.assertAlmostEqual(m.total_area([m.Rectangle(1, 2), m.Square(2)]), 6)

    def test_describe_extends_parent(self):
        self.assertEqual(m.Square(2).describe(), "Shape Rectangle Square")


class TestMRO(unittest.TestCase):
    def test_diamond_mro(self):
        self.assertEqual(m.diamond_mro(), ["D", "B", "C", "A", "object"])

    def test_cooperative_super_calls_each_once(self):
        self.assertEqual(m.D().hello(), ["D", "B", "C", "A"])


class TestMixin(unittest.TestCase):
    def test_json_mixin(self):
        self.assertEqual(m.Point(1, 2).to_json(), '{"x": 1, "y": 2}')

    def test_isinstance_issubclass(self):
        self.assertTrue(issubclass(m.Square, m.Shape))
        self.assertFalse(issubclass(m.Circle, m.Rectangle))


class TestClassVsInstance(unittest.TestCase):
    def test_class_attribute_shared_instance_attribute_not(self):
        a, b = m.Counter(), m.Counter()
        a.bump()
        self.assertEqual(m.Counter.created, 2)
        self.assertEqual((a.n, b.n), (1, 0))


class TestOverrideRegistry(unittest.TestCase):
    def test_init_subclass_registry(self):
        self.assertIn("Dog", m.Animal.registry)
        self.assertIs(m.Animal.registry["Cat"], m.Cat)
        self.assertEqual(m.Dog().speak(), "Woof")

class TestShapeEdges(unittest.TestCase):
    def test_zero_dimensions(self):
        self.assertEqual(m.Circle(0).area(), 0)
        self.assertEqual(m.Rectangle(0, 5).area(), 0)
        self.assertEqual(m.Square(0).area(), 0)

    def test_float_dimensions(self):
        self.assertAlmostEqual(m.Rectangle(0.5, 0.5).area(), 0.25)
        self.assertAlmostEqual(m.Circle(0.5).area(), math.pi / 4)

    def test_total_area_empty(self):
        self.assertEqual(m.total_area([]), 0)

    def test_total_area_accepts_generator(self):
        self.assertEqual(m.total_area(m.Square(i) for i in (1, 2)), 5)

    def test_circle_describe_uses_base(self):
        self.assertEqual(m.Circle(1).describe(), "Shape")

    def test_rectangle_describe(self):
        self.assertEqual(m.Rectangle(1, 2).describe(), "Shape Rectangle")

    def test_incomplete_subclass_cannot_instantiate(self):
        class Bad(m.Shape):
            pass
        with self.assertRaises(TypeError):
            Bad()

    def test_complete_subclass_can_instantiate(self):
        class Dot(m.Shape):
            def area(self):
                return 0
        self.assertEqual(Dot().area(), 0)

    def test_square_sides_are_independent_from_other_squares(self):
        a, b = m.Square(1), m.Square(2)
        a.w = 10
        self.assertEqual((b.w, b.h), (2, 2))

    def test_square_mro(self):
        self.assertEqual([c.__name__ for c in m.Square.__mro__], ["Square", "Rectangle", "Shape", "ABC", "object"])


class TestMROEdges(unittest.TestCase):
    def test_base_classes_alone(self):
        self.assertEqual(m.A().hello(), ["A"])
        self.assertEqual(m.B().hello(), ["B", "A"])
        self.assertEqual(m.C().hello(), ["C", "A"])

    def test_a_mro(self):
        self.assertEqual([c.__name__ for c in m.A.__mro__], ["A", "object"])

    def test_swapped_bases_change_order(self):
        class E(m.C, m.B):
            def hello(self):
                return ["E"] + super().hello()
        self.assertEqual(E().hello(), ["E", "C", "B", "A"])

    def test_inconsistent_hierarchy_rejected(self):
        with self.assertRaises(TypeError):
            type("Bad", (m.A, m.B), {})  # A before its subclass B: no valid linearization

    def test_diamond_a_called_once(self):
        self.assertEqual(m.D().hello().count("A"), 1)


class TestMixinEdges(unittest.TestCase):
    def test_none_and_str_values(self):
        self.assertEqual(m.Point(None, "s").to_json(), '{"x": null, "y": "s"}')

    def test_roundtrip(self):
        p = m.Point(1.5, -2)
        self.assertEqual(json.loads(p.to_json()), {"x": 1.5, "y": -2})

    def test_unserializable_value(self):
        with self.assertRaises(TypeError):
            m.Point(object(), 1).to_json()

    def test_reflects_later_attributes(self):
        p = m.Point(1, 2)
        p.z = 3
        self.assertEqual(json.loads(p.to_json()), {"x": 1, "y": 2, "z": 3})

    def test_mixin_alone_serializes_empty(self):
        self.assertEqual(m.JsonMixin().to_json(), "{}")


class TestCounterEdges(unittest.TestCase):
    def test_instance_attribute_shadows_class_attribute(self):
        a = m.Counter()
        a.created = 99  # creates an instance attribute only
        self.assertNotEqual(m.Counter.created, 99)
        self.assertEqual(m.Counter().created, m.Counter.created)

    def test_created_counts_every_instance(self):
        before = m.Counter.created
        [m.Counter() for _ in range(3)]
        self.assertEqual(m.Counter.created, before + 3)

    def test_bump_many(self):
        c = m.Counter()
        for _ in range(5):
            c.bump()
        self.assertEqual(c.n, 5)

    def test_subclass_shares_created(self):
        class Sub(m.Counter):
            pass
        before = m.Counter.created
        Sub()
        self.assertEqual(m.Counter.created, before + 1)


class TestAnimalEdges(unittest.TestCase):
    def test_base_speak_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            m.Animal().speak()

    def test_new_subclass_auto_registered(self):
        class Fish(m.Animal):
            def speak(self):
                return "..."
        self.assertIs(m.Animal.registry["Fish"], Fish)

    def test_sub_subclass_registered_and_inherits(self):
        class Puppy(m.Dog):
            pass
        self.assertIn("Puppy", m.Animal.registry)
        self.assertEqual(Puppy().speak(), "Woof")

    def test_override_via_super(self):
        class Loud(m.Dog):
            def speak(self):
                return super().speak().upper() + "!"
        self.assertEqual(Loud().speak(), "WOOF!")

    def test_base_not_registered(self):
        self.assertNotIn("Animal", m.Animal.registry)

    def test_isinstance_checks(self):
        self.assertIsInstance(m.Cat(), m.Animal)
        self.assertNotIsInstance(m.Cat(), m.Dog)
        self.assertFalse(issubclass(m.Animal, m.Dog))


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
