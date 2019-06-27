"""
Tests for detecting redefinition of builtins.
"""
from pyflakes import messages as m
from pyflakes.test.harness import TestCase, skipIf
from sys import version_info


class TestBuiltins(TestCase):
    def test_basic_method(self):
        self.flakes('''
        def foo(arg: int):
            a = 42
            b = a + arg
            a = a - b
        foo(0)
        ''')

    def test_no_args(self):
        self.flakes('''
        def foo():
            y = 0
            x = 7
            x = x + 1

            y = y + 1
            return x
        ''')

    def test_widening(self):
        self.flakes('''
        def foo():
            y = 0
            x = 7
            x = x + 1
            while input():
                x = 7
                x = x + 1
                y = y + 1
            return x
        ''')
