from pyflakes.boolean_lattice import Boolean


def interval_method(self, other, m):
    assert isinstance(other, Interval)
    if isinstance(other, Bottom):
        return other
    results = list(getattr(a, m)(b) for a in self for b in other)
    return Interval(min(results), max(results))


def bool_method(self, other, m):
    assert isinstance(other, Interval)
    if isinstance(other, Bottom):
        return other
    return Boolean(getattr(a, m)(b) for a in self for b in other)


class IntervalInt(object):
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        if isinstance(other, NegInfinityClass):
            return False
        return isinstance(other, InfinityClass) or self.value < other.value

    def __le__(self, other):
        if isinstance(other, NegInfinityClass):
            return False
        return isinstance(other, InfinityClass) or self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __add__(self, other):
        if isinstance(other, InfinityClass) or isinstance(other, NegInfinityClass):
            return other
        return IntervalInt(self.value + other.value)

    def __sub__(self, other):
        if isinstance(other, InfinityClass):
            return NEG_INFINITY
        if isinstance(other, NegInfinityClass):
            return INFINITY
        return IntervalInt(self.value - other.value)

    def __floordiv__(self, other):
        if isinstance(other, InfinityClass):
            return IntervalInt(0 if 0 <= self.value else -1)
        if isinstance(other, NegInfinityClass):
            return IntervalInt(0 if self.value <= 0 else -1)
        return IntervalInt(self.value // other.value)

    def __mul__(self, other):
        if self.value == 0:
            return IntervalInt(0)
        if isinstance(other, InfinityClass):
            if self.value > 0:
                return other
            else:
                return NEG_INFINITY
        if isinstance(other, NegInfinityClass):
            if self.value > 0:
                return other
            else:
                return INFINITY
        return IntervalInt(self.value * other.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class InfinityClass(IntervalInt):
    def __init__(self):
        super(InfinityClass, self).__init__(None)

    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return True

    def __eq__(self, other):
        return self is other

    def __le__(self, other):
        return self is other

    def __ge__(self, other):
        return True

    def __add__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __mul__(self, other):
        if other.value == 0 or isinstance(other, NegInfinityClass):
            return other
        if other.value is not None and other.value < 0:
            return NEG_INFINITY
        return self

    def __floordiv__(self, other):
        if isinstance(other, NegInfinityClass) or (other.value is not None and other.value < 0):
            return NEG_INFINITY
        return self

    def __str__(self):
        return "\u221E"


class NegInfinityClass(IntervalInt):
    def __init__(self):
        super(NegInfinityClass, self).__init__(None)

    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return False

    def __eq__(self, other):
        return self is other

    def __le__(self, other):
        return True

    def __ge__(self, other):
        return self is other

    def __add__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __mul__(self, other):
        if other.value == 0:
            return other
        if (other.value is not None and other.value < 0) or isinstance(other, NegInfinityClass):
            return INFINITY
        return self

    def __floordiv__(self, other):
        if (other.value is not None and other.value < 0) or isinstance(other, NegInfinityClass):
            return INFINITY
        return self

    def __str__(self):
        return "-\u221E"


ZERO_INT = IntervalInt(0)
INFINITY = InfinityClass()
NEG_INFINITY = NegInfinityClass()


class Interval(object):
    def __init__(self, begin, end=None):
        assert end is None if begin is None else isinstance(begin, (int, IntervalInt))
        assert not isinstance(begin, InfinityClass) or not isinstance(end, InfinityClass)
        assert not isinstance(begin, NegInfinityClass) or not isinstance(end, NegInfinityClass)

        self.begin = IntervalInt(begin) if isinstance(begin, int) else begin

        if end is not None:
            assert isinstance(end, (int, IntervalInt))
            self.end = IntervalInt(end) if isinstance(end, int) else end
        else:
            assert not isinstance(begin, (InfinityClass, NegInfinityClass))
            self.end = self.begin

        assert self.begin <= self.end

    def debug_checks(self, other):
        assert isinstance(other, Interval)

    def is_none(self):
        return self.begin is None

    def __iter__(self):
        yield self.begin
        yield self.end

    def __eq__(self, other):
        self.debug_checks(other)
        if isinstance(other, Bottom):
            return other
        return Boolean(
            self.begin == other.begin == self.end == other.end,
            self.begin <= other.end and other.begin <= self.end,
        )

    def equals(self, other):
        return self.begin == other.begin and self.end == other.end

    def __str__(self):
        return f"({str(self.begin)}, {str(self.end)})"

    def __repr__(self):
        return str(self)

    def __ne__(self, other):
        self.debug_checks(other)
        return ~(self == other)

    def __floordiv__(self, other):
        self.debug_checks(other)
        if isinstance(other, Bottom):
            return other
        if ZERO.equals(other):
            raise ZeroDivisionError()
        if ZERO_INT == other.begin:
            return self // Interval(1, other.end)
        if ZERO_INT == other.end:
            return self // Interval(other.begin, -1)
        if other.begin < ZERO_INT < other.end:
            return (self // Interval(other.begin, -1)).join(self // Interval(1, other.end))
        results = list(getattr(a, "__floordiv__")(b) for a in self for b in other)
        return Interval(min(results), max(results))

    def join(self, other):
        self.debug_checks(other)
        return Interval(min(self.begin, other.begin), max(self.end, other.end))

    def intersection(self, other):
        self.debug_checks(other)
        if self.end < other.begin or other.end < self.begin:
            return BOTTOM
        return Interval(max(self.begin, other.begin), min(self.end, other.end))

    def __add__(self, other):
        return interval_method(self, other, "__add__")

    def __sub__(self, other):
        return interval_method(self, other, "__sub__")

    def __mul__(self, other):
        return interval_method(self, other, "__mul__")

    def __gt__(self, other):
        return bool_method(self, other, "__gt__")

    def __ge__(self, other):
        return bool_method(self, other, "__ge__")

    def __lt__(self, other):
        return bool_method(self, other, "__lt__")

    def __le__(self, other):
        return bool_method(self, other, "__le__")


class Bottom(Interval):
    # TODO implement this
    def __init__(self):
        super(Bottom, self).__init__(0, 0)

    def __str__(self):
        return "⊥"

    def __add__(self, other):
        return self

    __sub__ = __mul__ = __gt__ = __ge__ = __lt__ = __le__ = __eq__ = __floordiv__ = __add__


ZERO = Interval(ZERO_INT)
TOP = Interval(NEG_INFINITY, INFINITY)
BOTTOM = Bottom()
GIVE_BOTTOM = lambda _x: BOTTOM
GIVE_TOP = lambda _x: TOP