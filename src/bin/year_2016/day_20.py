from bisect import bisect
from collections import deque
from itertools import takewhile
from operator import attrgetter


class Range:

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

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


def part_1(text):
    ranges = []
    for line in text.strip().split("\n"):
        ranges.append(Range(*map(int, line.split("-"))))

    ranges = deque(sorted(ranges, key=attrgetter("start")))
    result = 0
    while ranges:
        range_ = ranges.popleft()
        if result in range_:
            result = range_.stop + 1
        elif range_.stop < result:
            pass
        elif range_.start > result:
            return result
    return result


def add_range(ranges, range_):
    """
    add range into a list of ranges, so it stays sorted by start, and there is no overlap
    between ranges.
    If the new range overlaps with some ranges, they are merged into a single one.
    """
    index = bisect(ranges, range_.as_tuple, key=attrgetter("as_tuple"))

    union_left = ranges[index - 1].union(range_) if index > 0 else None

    union_right = range_
    count = 0
    for right_range in takewhile(lambda r: r.start <= range_.stop + 1, ranges[index:]):
        union_right = union_right.union(right_range)
        count += 1

    if union_left:
        return [
            *ranges[: index - 1],
            union_left.union(union_right),
            *ranges[index + count :],
        ]
    else:
        return [*ranges[:index], union_right, *ranges[index + count :]]


def part_2(text):
    ranges = []

    for line in text.strip().split("\n"):
        range_ = Range(*map(int, line.split("-")))
        ranges = add_range(ranges, range_)

    return 2**32 - sum(map(len, ranges))
