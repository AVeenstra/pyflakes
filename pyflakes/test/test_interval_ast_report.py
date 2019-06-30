"""
Tests for detecting redefinition of builtins.
"""
from pyflakes.test.harness import TestCase
from pyflakes.messages import DivisionByZero, DeadCode


class TestBuiltins(TestCase):

    def test_divide_by_zero(self):
        with self.assertRaisesRegex(AssertionError, DivisionByZero.message):
            self.flakes('''
            def foo():
                y = 0
                x = 7
                y = x // y
            ''')

    def test_divide_by_zero_addition(self):
        with self.assertRaisesRegex(AssertionError, DivisionByZero.message):
            self.flakes('''
            def foo():
                x = -5
                y = 5
                y = 5 // (x + y)
            ''')

    def test_divide_by_zero_computed(self):
        with self.assertRaisesRegex(AssertionError, DivisionByZero.message):
            self.flakes('''
            def foo():
                y = 1
                x = 1
                y = x // (y-x)
            ''')

    def test_divide_by_zero_multiplication(self):
        with self.assertRaisesRegex(AssertionError, DivisionByZero.message):
            self.flakes('''
            def foo():
                x = 2
                y = x // (x * 0)
            ''')

    def test_divide_by_zero_floor(self):
        with self.assertRaisesRegex(AssertionError, DivisionByZero.message):
            self.flakes('''
            def foo():
                y = 1
                x = 2
                y = x // (y // x)
            ''')

    def test_divide_by_zero_method(self):
        with self.assertRaisesRegex(AssertionError, DivisionByZero.message):
            self.flakes('''
            def min(arg: int):
                return arg - 1
            
            def foo():
                1 // min(1)
            ''')

    def test_dead_code_if(self):
        with self.assertRaisesRegex(AssertionError, DeadCode.message):
            self.flakes('''
            def foo():
                a = False
                b = 1
                if(a):
                    b = b + b
            ''')

    def test_dead_code_elif(self):
        with self.assertRaisesRegex(AssertionError, DeadCode.message):
            self.flakes('''
            def foo(arg: bool):
                a = False
                b = 1
                if(arg):
                    b = b + b
                elif(a):
                    b = b + b
            ''')

    def test_dead_code_else(self):
        with self.assertRaisesRegex(AssertionError, DeadCode.message):
            self.flakes('''
            def foo():
                a = True
                b = 1
                if(a):
                    b = b + b
                else:
                    b = b + b
            ''')
