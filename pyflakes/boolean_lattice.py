class Boolean:
    def __init__(self, *value):
        assert all(isinstance(v, bool) for v in value)
        self.value = set(value)

    def __str__(self):
        return str(self.value)

    def __iter__(self):
        return self.value.__iter__()

    def __neg__(self):
        return Boolean()

    def __bool__(self):
        raise Exception("Booleans can not be cast to Python bools")


B_TOP = Boolean(True, False)
TRUE = Boolean(True)
FALSE = Boolean(False)
B_BOT = Boolean()


def get_method(m):
    def apply(self, other):
        assert isinstance(other, Boolean)
        results = list(getattr(a, m)(b) for a in self for b in other)
        return Boolean(*results)

    return apply


for method in ["__eq__", "__ne__", "__and__", "__or__", "__xor__"]:
    setattr(Boolean, method, get_method(method))
