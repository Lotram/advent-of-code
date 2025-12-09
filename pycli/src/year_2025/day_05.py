from pycli.src.ranges import MultiRange, Range


def part_1(text, example: bool = False):
    _ranges, values = text.split("\n\n")
    ranges = [Range.from_text(line) for line in _ranges.splitlines()]
    multirange = MultiRange(ranges)
    result = sum(1 for value in map(int, values.splitlines()) if value in multirange)

    return result


def part_2(text, example: bool = False):
    _ranges, _ = text.split("\n\n")
    ranges = [Range.from_text(line) for line in _ranges.splitlines()]
    multirange = MultiRange(ranges)

    result = len(multirange)
    return result
