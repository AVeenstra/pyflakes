from typing import Any

from pyflakes.boolean_lattice import TRUE, FALSE, Boolean
from pyflakes.test.harness import TestCase


class TestInterval(TestCase):
    def assertEqual(self, first: Boolean, second: Boolean, msg: Any = ...) -> None:
        super(TestInterval, self).assertEqual(first.value, second.value, msg)

    def test_bool(self):
        self.assertEqual(TRUE & FALSE, FALSE)
