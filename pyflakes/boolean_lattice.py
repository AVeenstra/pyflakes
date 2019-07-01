def bool_method(self, other, m):
    assert isinstance(other, Boolean)
    results = list(getattr(a, m)(b) for a in self for b in other)
    return Boolean(*results)


class Boolean:
    def __init__(self, *value):
        self.value = set()
        self.unravel(value)

    def unravel(self, value):
        try:
            for v in value:
                if isinstance(v, bool):
                    self.value.add(v)
                elif isinstance(v, Boolean):
                    self.value.update(v.value)
                else:
                    self.unravel(v)
        except Exception as e:
            print("Value that caused an exception:", value)
            raise e

    def equals(self, other):
        return self.value == other.value

    def join(self, other):
        assert isinstance(other, Boolean)
        return Boolean(self.value, other.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self.value.__iter__()

    def __bool__(self):
        if self.value == {True}:
            return True
        elif self.value == {False}:
            return False
        raise Exception("Booleans can not be cast to Python bools")

    def __eq__(self, other):
        return bool_method(self, other, "__eq__")

    def __ne__(self, other):
        return bool_method(self, other, "__ne__")

    def __and__(self, other):
        return bool_method(self, other, "__and__")

    def __or__(self, other):
        return bool_method(self, other, "__or__")

    def __xor__(self, other):
        return bool_method(self, other, "__xor__")

    def __invert__(self):
        return Boolean(not v for v in self.value)


BOOLEAN_TOP = Boolean(True, False)
TRUE = Boolean(True)
FALSE = Boolean(False)
BOOLEAN_BOTTOM = Boolean()

GIVE_BOOLEAN_BOTTOM = lambda _x: BOOLEAN_BOTTOM
GIVE_BOOLEAN_TOP = lambda _x: BOOLEAN_TOP
