from typing import Any

from pyflakes.boolean_lattice import TRUE, FALSE, Boolean, BOOLEAN_TOP, BOOLEAN_BOTTOM
from pyflakes.test.harness import TestCase


class TestInterval(TestCase):
    def assertEqual(self, first: Boolean, second: Boolean, msg: Any = ...) -> None:
        super(TestInterval, self).assertEqual(first.value, second.value, msg)

    def test_AND(self):
        self.assertEqual(FALSE & FALSE, FALSE)
        self.assertEqual(TRUE & FALSE, FALSE)
        self.assertEqual(FALSE & TRUE, FALSE)
        self.assertEqual(TRUE & TRUE, TRUE)

        self.assertEqual(BOOLEAN_TOP & TRUE, BOOLEAN_TOP)
        self.assertEqual(BOOLEAN_TOP & FALSE, FALSE)
        self.assertEqual(BOOLEAN_BOTTOM & TRUE, BOOLEAN_BOTTOM)
        self.assertEqual(BOOLEAN_BOTTOM & FALSE, BOOLEAN_BOTTOM)

    def test_OR(self):
        self.assertEqual(FALSE | FALSE, FALSE)
        self.assertEqual(TRUE | FALSE, TRUE)
        self.assertEqual(FALSE | TRUE, TRUE)
        self.assertEqual(TRUE | TRUE, TRUE)

        self.assertEqual(BOOLEAN_TOP | TRUE, TRUE)
        self.assertEqual(BOOLEAN_TOP | FALSE, BOOLEAN_TOP)
        self.assertEqual(BOOLEAN_BOTTOM | TRUE, TRUE)
        self.assertEqual(BOOLEAN_BOTTOM | FALSE, BOOLEAN_BOTTOM)

    def test_equal(self):
        self.assertEqual(FALSE == FALSE, TRUE)
        self.assertEqual(TRUE == FALSE, FALSE)
        self.assertEqual(FALSE == TRUE, FALSE)
        self.assertEqual(TRUE == TRUE, TRUE)

        self.assertEqual(BOOLEAN_TOP == TRUE, BOOLEAN_TOP)
        self.assertEqual(BOOLEAN_TOP == FALSE, BOOLEAN_TOP)
        self.assertEqual(BOOLEAN_BOTTOM == TRUE, BOOLEAN_BOTTOM)
        self.assertEqual(BOOLEAN_BOTTOM == FALSE, BOOLEAN_BOTTOM)

    def test_NOT_equal(self):
        self.assertEqual(FALSE != FALSE, FALSE)
        self.assertEqual(TRUE != FALSE, TRUE)
        self.assertEqual(FALSE != TRUE, TRUE)
        self.assertEqual(TRUE != TRUE, FALSE)

        self.assertEqual(BOOLEAN_TOP != TRUE, BOOLEAN_TOP)
        self.assertEqual(BOOLEAN_TOP != FALSE, BOOLEAN_TOP)
        self.assertEqual(BOOLEAN_BOTTOM != TRUE, BOOLEAN_BOTTOM)
        self.assertEqual(BOOLEAN_BOTTOM != FALSE, BOOLEAN_BOTTOM)
