"""
Tests for detecting redefinition of builtins.
"""
from pyflakes.test.harness import TestCase
from pyflakes import messages as m


class TestIntervalAST(TestCase):
    def test_basic_method_args(self):
            self.flakes('''
            def foo(arg: int):
                a = 42
                b = a + arg
                a = a - b
            foo(0)
        ''')

    def test_basic_method_bool(self):
            self.flakes('''
            def foo(arg: bool):
                a = 42
                b = a + 7
                if arg:
                    a = 0
            foo(0)
        ''', m.UnusedVariable)

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

    def test_divide_by_zero(self):
        self.flakes('''
        def foo():
            y = 0
            x = 7
            y = x // y
        ''', m.DivisionByZero)

    def test_divide_by_zero_computed(self):
        self.flakes('''
        def foo():
            y = 1
            x = 1
            y = x // (y - x)
        ''', m.DivisionByZero)

    def test_divide_by_zero_floor(self):
        self.flakes('''
        def foo():
            y = 1
            x = 2
            y = x // (y // x)
        ''', m.DivisionByZero)

    def test_divide_by_zero_multiplication(self):
        self.flakes('''
        def foo():
            x = 2
            x = x // (x * 0)
        ''', m.DivisionByZero)

    def test_divide_by_zero_addition(self):
        self.flakes('''
        def foo():
            x = -5
            y = 5
            y = 5 // (x + y)
        ''', m.DivisionByZero)
