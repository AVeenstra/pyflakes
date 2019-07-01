from pyflakes.interval import Interval, INFINITY, NEG_INFINITY, TOP, BOTTOM
from pyflakes.boolean_lattice import TRUE, FALSE, BOOLEAN_TOP, BOOLEAN_BOTTOM
from pyflakes.test.harness import TestCase


class TestIntervalComparator(TestCase):
    def assertEqual(self, first: Interval, second: Interval, msg=...) -> None:
        super(TestIntervalComparator, self).assertEqual(str(first), str(second), msg)

    def test_smaller(self):
        self.assertEqual(Interval(5) < Interval(6), TRUE)
        self.assertEqual(Interval(-1) < Interval(1), TRUE)
        self.assertEqual(Interval(0) < Interval(-1), FALSE)
        self.assertEqual(Interval(1) < Interval(1), FALSE)

    def test_smaller_interval(self):
        self.assertEqual(Interval(1, 2) < Interval(5, 6), TRUE)
        self.assertEqual(Interval(5, 6) < Interval(1, 2), FALSE)
        self.assertEqual(Interval(2, 5) < Interval(4, 6), BOOLEAN_TOP)
        self.assertEqual(Interval(2, 5) < Interval(3, 4), BOOLEAN_TOP)
        self.assertEqual(Interval(3, 4) < Interval(2, 5), BOOLEAN_TOP)

    def test_greater(self):
        self.assertEqual(Interval(0) > Interval(-1), TRUE)
        self.assertEqual(Interval(-1) > Interval(1), FALSE)
        self.assertEqual(Interval(5) > Interval(6), FALSE)
        self.assertEqual(Interval(1) > Interval(1), FALSE)

    def test_greater_interval(self):
        self.assertEqual(Interval(5, 6) > Interval(1, 2), TRUE)
        self.assertEqual(Interval(1, 2) > Interval(5, 6), FALSE)
        self.assertEqual(Interval(2, 5) > Interval(4, 6), BOOLEAN_TOP)
        self.assertEqual(Interval(2, 5) > Interval(3, 4), BOOLEAN_TOP)
        self.assertEqual(Interval(3, 4) > Interval(2, 5), BOOLEAN_TOP)

    def test_equals(self):
        self.assertEqual(Interval(0) == Interval(0), TRUE)
        self.assertEqual(Interval(-1) == Interval(1), FALSE)
        self.assertEqual(Interval(0) == Interval(-1), FALSE)

    def test_equals_interval(self):
        self.assertEqual(Interval(1, 3) == Interval(1, 3), BOOLEAN_TOP)
        self.assertEqual(Interval(1, 2) == Interval(2, 3), BOOLEAN_TOP)
        self.assertEqual(Interval(1, 2) == Interval(3, 5), FALSE)

    def test_nequals(self):
        self.assertEqual(Interval(0) != Interval(0), FALSE)
        self.assertEqual(Interval(-1) != Interval(1), TRUE)
        self.assertEqual(Interval(0) != Interval(-1), TRUE)

    def test_nequals_interval(self):
        self.assertEqual(Interval(1, 3) != Interval(1, 3), BOOLEAN_TOP)
        self.assertEqual(Interval(1, 2) != Interval(2, 3), BOOLEAN_TOP)
        self.assertEqual(Interval(1, 2) != Interval(3, 5), TRUE)

    def test_infinity_comparators_report(self):
        self.assertEqual(Interval(0, INFINITY) == Interval(0, INFINITY), TRUE)
        self.assertEqual(Interval(NEG_INFINITY, 0) != Interval(0, INFINITY), TRUE)
        self.assertEqual(Interval(0, INFINITY) > Interval(NEG_INFINITY, 0), TRUE)
        self.assertEqual(Interval(0, INFINITY) >= Interval(NEG_INFINITY, 0), TRUE)
        self.assertEqual(Interval(NEG_INFINITY, 0) < Interval(0, INFINITY), TRUE)
        self.assertEqual(Interval(NEG_INFINITY, 0) <= Interval(0, INFINITY), TRUE)
        self.assertEqual(Interval(0, INFINITY) > Interval(999999), TRUE)
        self.assertEqual(Interval(0, INFINITY) >= Interval(999999), TRUE)
        self.assertEqual(Interval(NEG_INFINITY, 0) < Interval(-999999), TRUE)
        self.assertEqual(Interval(NEG_INFINITY, 0) <= Interval(-999999), TRUE)

    def test_infinity_comparators_report_false(self):
        self.assertEqual(Interval(0, INFINITY) != Interval(0, INFINITY), FALSE)
        self.assertEqual(Interval(NEG_INFINITY, 0) == Interval(0, INFINITY), FALSE)
        self.assertEqual(Interval(0, INFINITY) < Interval(NEG_INFINITY, 0), FALSE)
        self.assertEqual(Interval(0, INFINITY) <= Interval(NEG_INFINITY, 0), FALSE)
        self.assertEqual(Interval(NEG_INFINITY, 0) > Interval(0, INFINITY), FALSE)
        self.assertEqual(Interval(NEG_INFINITY, 0) >= Interval(0, INFINITY), FALSE)
        self.assertEqual(Interval(0, INFINITY) < Interval(999999), FALSE)
        self.assertEqual(Interval(0, INFINITY) <= Interval(999999), FALSE)
        self.assertEqual(Interval(NEG_INFINITY, 0) > Interval(-999999), FALSE)
        self.assertEqual(Interval(NEG_INFINITY, 0) >= Interval(-999999), FALSE)

    def test_TOP_comparators(self):
        self.assertEqual(TOP >= Interval(1, 2), BOOLEAN_TOP)
        self.assertEqual(TOP > Interval(1, 2), BOOLEAN_TOP)
        self.assertEqual(TOP <= Interval(1, 2), BOOLEAN_TOP)
        self.assertEqual(TOP < Interval(1, 2), BOOLEAN_TOP)
        self.assertEqual(TOP == Interval(1, 2), BOOLEAN_TOP)
        self.assertEqual(TOP != Interval(1, 2), BOOLEAN_TOP)
        self.assertEqual(TOP == TOP, BOOLEAN_TOP)

    def test_BOTTOM_comparators(self):
        self.assertEqual(BOTTOM >= Interval(1,2), BOOLEAN_BOTTOM)
        self.assertEqual(BOTTOM > Interval(1, 2), BOOLEAN_BOTTOM)
        self.assertEqual(BOTTOM <= Interval(1, 2), BOOLEAN_BOTTOM)
        self.assertEqual(BOTTOM < Interval(1, 2), BOOLEAN_BOTTOM)
        self.assertEqual(BOTTOM == Interval(1, 2), BOOLEAN_BOTTOM)
        self.assertEqual(BOTTOM != Interval(1, 2), BOOLEAN_BOTTOM)
        self.assertEqual(BOTTOM == BOTTOM, BOOLEAN_BOTTOM)
