from collections import deque
from operator import attrgetter

from pycli.src.ranges import MultiRange, Range


def part_1(text, example: bool = False):
    ranges = []
    ranges = [Range.from_text(line) for line in text.strip().split("\n")]

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


def part_2(text, example: bool = False):
    ranges = []
    ranges = [Range.from_text(line) for line in text.strip().split("\n")]
    multi_range = MultiRange(ranges)

    return 2**32 - len(multi_range)
