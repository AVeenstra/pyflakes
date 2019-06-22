from pyflakes.interval import Interval, INFINITY, NEG_INFINITY
from pyflakes.test.harness import TestCase


class TestInterval(TestCase):
    def test_plus(self):
        self.assertEqual(Interval(-10, 1) + Interval(-1, 2), Interval(-11, 3))
        self.assertEqual(Interval(1) + Interval(2), Interval(3))

    def test_plus_infinity(self):
        self.assertEqual(Interval(NEG_INFINITY, 1) + Interval(-1, 2), Interval(NEG_INFINITY, 3))
        self.assertEqual(Interval(-10, INFINITY) + Interval(-1, 2), Interval(-11, INFINITY))
        self.assertEqual(Interval(-10, 1) + Interval(NEG_INFINITY, 2), Interval(NEG_INFINITY, 3))
        self.assertEqual(Interval(-10, 1) + Interval(-1, INFINITY), Interval(-11, INFINITY))
        self.assertEqual(Interval(0, INFINITY) + Interval(2), Interval(2, INFINITY))
        self.assertEqual(Interval(NEG_INFINITY, 0) + Interval(2), Interval(NEG_INFINITY, 2))
        self.assertEqual(Interval(1) + Interval(0, INFINITY), Interval(1, INFINITY))
        self.assertEqual(Interval(1) + Interval(NEG_INFINITY, 0), Interval(NEG_INFINITY, 1))

    def test_plus_top(self):
        self.assertEqual(
            Interval(NEG_INFINITY, INFINITY) + Interval(NEG_INFINITY, INFINITY),
            Interval(NEG_INFINITY, INFINITY)
        )

    def test_minus(self):
        self.assertEqual(Interval(-10, 1) - Interval(-1, 2), Interval(-12, 2))
        self.assertEqual(Interval(1) - Interval(2), Interval(-1))

    def test_minus_infinity_simple(self):
        self.assertEqual(Interval(NEG_INFINITY, 1) - Interval(-1, 2), Interval(NEG_INFINITY, 2))
        self.assertEqual(Interval(-10, INFINITY) - Interval(-1, 2), Interval(-12, INFINITY))
        self.assertEqual(Interval(0, INFINITY) - Interval(2), Interval(-2, INFINITY))
        self.assertEqual(Interval(NEG_INFINITY, 0) - Interval(2), Interval(NEG_INFINITY, -2))

    def test_minus_infinity(self):
        self.assertEqual(Interval(-10, 1) - Interval(NEG_INFINITY, 2), Interval(-12, INFINITY))
        self.assertEqual(Interval(-10, 1) - Interval(-1, INFINITY), Interval(NEG_INFINITY, 2))
        self.assertEqual(Interval(0, INFINITY) - Interval(NEG_INFINITY, 0), Interval(0, INFINITY))
        self.assertEqual(Interval(2) - Interval(NEG_INFINITY, INFINITY), Interval(NEG_INFINITY, INFINITY))
        self.assertEqual(Interval(NEG_INFINITY, INFINITY) - Interval(2), Interval(NEG_INFINITY, INFINITY))
        self.assertEqual(Interval(1) - Interval(0, INFINITY), Interval(NEG_INFINITY, 1))
        self.assertEqual(Interval(1) - Interval(NEG_INFINITY, 0), Interval(1, INFINITY))

    def test_minus_infinity_top(self):
        self.assertEqual(
            Interval(NEG_INFINITY, INFINITY) - Interval(NEG_INFINITY, INFINITY),
            Interval(NEG_INFINITY, INFINITY)
        )

    def test_mul(self):
        self.assertEqual(Interval(-10, 1) * Interval(-1, 2), Interval(-20, 10))
        self.assertEqual(Interval(1) * Interval(2), Interval(2))

    def test_mul_infinity_simple(self):
        self.assertEqual(Interval(NEG_INFINITY, 1) * Interval(-1, 2), Interval(NEG_INFINITY, INFINITY))
        self.assertEqual(Interval(-10, INFINITY) * Interval(-1, 2), Interval(NEG_INFINITY, INFINITY))
        self.assertEqual(Interval(0, INFINITY) * Interval(2), Interval(0, INFINITY))
        self.assertEqual(Interval(NEG_INFINITY, 0) * Interval(2), Interval(NEG_INFINITY, 0))
        self.assertEqual(Interval(NEG_INFINITY, 0) * Interval(0), Interval(0))
        self.assertEqual(Interval(0, INFINITY) * Interval(0), Interval(0))
        self.assertEqual(Interval(0) * Interval(0, INFINITY), Interval(0))
        self.assertEqual(Interval(0) * Interval(NEG_INFINITY, 0), Interval(0))

    def test_mul_infinity(self):
        self.assertEqual(Interval(-10, 1) * Interval(NEG_INFINITY, 2), Interval(NEG_INFINITY, INFINITY))
        self.assertEqual(Interval(-10, 1) * Interval(-1, INFINITY), Interval(NEG_INFINITY, INFINITY))
        self.assertEqual(Interval(0, INFINITY) * Interval(NEG_INFINITY, 0), Interval(NEG_INFINITY, 0))
        self.assertEqual(Interval(2) * Interval(NEG_INFINITY, INFINITY), Interval(NEG_INFINITY, INFINITY))
        self.assertEqual(Interval(NEG_INFINITY, INFINITY) * Interval(2), Interval(NEG_INFINITY, INFINITY))
        self.assertEqual(Interval(1) * Interval(0, INFINITY), Interval(0, INFINITY))
        self.assertEqual(Interval(1) * Interval(NEG_INFINITY, 0), Interval(NEG_INFINITY, 0))

    def test_mul_infinity_top(self):
        self.assertEqual(
            Interval(NEG_INFINITY, INFINITY) * Interval(NEG_INFINITY, INFINITY),
            Interval(NEG_INFINITY, INFINITY)
        )

    def test_div(self):
        self.assertEqual(Interval(-10, 1) // Interval(1, 2), Interval(-10, 1))
        self.assertEqual(Interval(-10, 1) // Interval(-2, -1), Interval(-1, 10))
        self.assertEqual(Interval(1) // Interval(2), Interval(0))

        with self.assertRaises(AssertionError):
            Interval(10, 20) // Interval(-10, 10)

    def test_div_infinity(self):
        pass
