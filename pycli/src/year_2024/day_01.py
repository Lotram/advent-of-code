from collections import Counter


def parse(text):
    left, right = zip(*(map(int, line.split()) for line in text.strip().splitlines()))
    return left, right


def part_1(text, example: bool = False):
    left, right = map(sorted, parse(text))
    result = sum(abs(_left - _right) for _left, _right in zip(left, right))
    return result


def part_2(text, example: bool = False):
    left, right = map(sorted, parse(text))
    counter = Counter(right)
    result = sum(_left * counter.get(_left, 0) for _left in left)
    return result
