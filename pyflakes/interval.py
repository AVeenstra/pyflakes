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
        if isinstance(other, (InfinityClass, NegInfinityClass)):
            return IntervalInt(0)
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
            assert begin <= end
            self.end = IntervalInt(end) if isinstance(end, int) else end
        else:
            assert not isinstance(begin, (InfinityClass, NegInfinityClass))
            self.end = self.begin

    def debug_checks(self, other):
        assert isinstance(other, Interval)

    def is_none(self):
        return self.begin is None

    def __iter__(self):
        yield self.begin
        yield self.end

    def __eq__(self, other):
        self.debug_checks(other)
        return self.begin == other.begin and self.end == other.end

    def __str__(self):
        return f"({str(self.begin)}, {str(self.end)})"

    def __repr__(self):
        return str(self)

    def __ne__(self, other):
        self.debug_checks(other)
        return self.begin != other.begin or self.end != other.end

    def __floordiv__(self, other):
        # TODO: Ignore divide by zero
        self.debug_checks(other)
        assert IntervalInt(0) < other.begin or other.end < IntervalInt(0)
        results = list(getattr(a, "__floordiv__")(b) for a in self for b in other)
        return Interval(min(results), max(results))


def get_method(m):
    def apply(self, other):
        assert isinstance(other, Interval)
        results = list(getattr(a, m)(b) for a in self for b in other)
        return Interval(min(results), max(results))

    return apply


for method in ["__add__", "__sub__", "__mul__"]:
    setattr(Interval, method, get_method(method))
