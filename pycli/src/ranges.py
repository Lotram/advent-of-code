from bisect import bisect
from collections.abc import Iterable
from itertools import takewhile
from operator import attrgetter


class Range:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    @classmethod
    def from_text(cls, input: str):
        return cls(*map(int, input.split("-")))

    def __contains__(self, value: int):
        return self.start <= value <= self.stop

    @property
    def as_tuple(self):
        return (self.start, self.stop)

    def union(self, other):
        if (
            self.start <= other.start <= self.stop + 1
            or other.start <= self.start <= other.stop + 1
        ):
            return Range(min(self.start, other.start), max(self.stop, other.stop))

    def __len__(self):
        return self.stop - self.start + 1

    def __repr__(self):
        return f"Range(start={self.start}, stop={self.stop})"


class MultiRange:
    def __init__(self, ranges: Iterable[Range]):
        self.ranges = []
        for range_ in ranges:
            self.add_range(range_)

    def add_range(self, range_):
        """
        add range into a list of ranges, so it stays sorted by start, and there is no overlap
        between ranges.
        If the new range overlaps with some ranges, they are merged into a single one.
        """
        index = bisect(self.ranges, range_.as_tuple, key=attrgetter("as_tuple"))

        union_left = self.ranges[index - 1].union(range_) if index > 0 else None

        union_right = range_
        count = 0
        for right_range in takewhile(
            lambda r: r.start <= range_.stop + 1, self.ranges[index:]
        ):
            union_right = union_right.union(right_range)
            count += 1

        if union_left:
            self.ranges = [
                *self.ranges[: index - 1],
                union_left.union(union_right),
                *self.ranges[index + count :],
            ]
        else:
            self.ranges = [
                *self.ranges[:index],
                union_right,
                *self.ranges[index + count :],
            ]

    def __len__(self):
        return sum(len(_range) for _range in self.ranges)

    def __contains__(self, value: int):
        return any(value in _range for _range in self.ranges)
