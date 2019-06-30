from typing import Any

from pyflakes.boolean_lattice import TRUE, FALSE, Boolean
from pyflakes.test.harness import TestCase


class TestInterval(TestCase):
    def assertEqual(self, first: Boolean, second: Boolean, msg: Any = ...) -> None:
        super(TestInterval, self).assertEqual(first.value, second.value, msg)

    def test_AND(self):
        self.assertEqual(FALSE & FALSE, FALSE)
        self.assertEqual(TRUE & FALSE, FALSE)
        self.assertEqual(FALSE & TRUE, FALSE)
        self.assertEqual(TRUE & TRUE, TRUE)

    def test_OR(self):
        self.assertEqual(FALSE | FALSE, FALSE)
        self.assertEqual(TRUE | FALSE, TRUE)
        self.assertEqual(FALSE | TRUE, TRUE)
        self.assertEqual(TRUE | TRUE, TRUE)

    def test_equal(self):
        self.assertEqual(FALSE == FALSE, TRUE)
        self.assertEqual(TRUE == FALSE, FALSE)
        self.assertEqual(FALSE == TRUE, FALSE)
        self.assertEqual(TRUE == TRUE, TRUE)

    def test_NOT_equal(self):
        self.assertEqual(FALSE != FALSE, FALSE)
        self.assertEqual(TRUE != FALSE, TRUE)
        self.assertEqual(FALSE != TRUE, TRUE)
        self.assertEqual(TRUE != TRUE, FALSE)
