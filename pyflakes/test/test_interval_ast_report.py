"""
Tests for detecting redefinition of builtins.
"""
from pyflakes.test.harness import TestCase
from pyflakes import messages as m


class TestBuiltins(TestCase):

    def test_divide_by_zero(self):
        self.flakes('''
        def foo():
            y = 0
            x = 7
            y = x // y
        ''', m.DivisionByZero)

    def test_divide_by_zero_addition(self):
        self.flakes('''
        def foo():
            x = -5
            y = 5
            y = 5 // (x + y)
        ''', m.DivisionByZero)

    def test_divide_by_zero_computed(self):
        self.flakes('''
        def foo():
            y = 1
            x = 1
            y = x // (y-x)
        ''', m.DivisionByZero)

    def test_divide_by_zero_multiplication(self):
        self.flakes('''
        def foo():
            x = 2
            x = x // (x * 0)
        ''', m.DivisionByZero)

    def test_divide_by_zero_floor(self):
        self.flakes('''
        def foo():
            y = 1
            x = 2
            y = x // (y // x)
        ''', m.DivisionByZero)

    def test_divide_by_zero_method(self):
        self.flakes('''
        def min(arg: int):
            return arg - 1
        
        def foo():
            1 // min(1)
        ''', m.DivisionByZero)

    def test_dead_code_if(self):
        self.flakes('''
        def foo():
            a = False
            b = 1
            if(a):
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_elif(self):
        self.flakes('''
        def foo(arg: bool):
            a = False
            b = 1
            if(arg):
                b = b + b
            elif(a):
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_else(self):
        self.flakes('''
        def foo():
            a = True
            b = 1
            if(a):
                b = b + b
            else:
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_method(self):
        self.flakes('''
        def t():
            return False
        
        def foo():
            a = True
            b = 1
            if(t()):
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_and(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if(a & c):
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_or(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if(c | c | c | c | a):
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_equals(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if(c == a):
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_if_if(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if(a):
                if(a):
                    if(c):
                        b = b + b
        ''', m.DeadCode)

    def test_dead_code_if_elif(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if(a):
                if(a):
                    b = b + b
                elif(c):
                    b = b + b
        ''', m.DeadCode)

    def test_dead_code_if_elif(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if(a):
                if(a):
                    b = b + b
                elif(a & c):
                    b = b + b
        ''', m.DeadCode)

    def test_dead_code_ifif(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if(a):
                b = b + b
            if(c):
                b = b + b                        
        ''', m.DeadCode)



