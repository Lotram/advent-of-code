import json
from functools import cmp_to_key


def sign(left, right):
    return int(left > right) - int(right > left)


def compare(left, right):
    match (left, right):
        case int(), int():
            return sign(left, right)
        case list(), list():
            for _left, _right in zip(left, right, strict=False):
                res = compare(_left, _right)
                if res != 0:
                    return res
            return sign(len(left), len(right))
        case list(), int():
            return compare(left, [right])
        case int(), list():
            return compare([left], right)


def part_1(text, example: bool = False):
    pairs = text.strip().split("\n\n")
    return sum(
        idx
        for idx, pair in enumerate(pairs, start=1)
        if compare(*map(json.loads, pair.split("\n"))) == -1
    )


def part_2(text, example: bool = False):
    dividers = ([[2]], [[6]])
    packets = [json.loads(line) for line in text.strip().split("\n") if line]
    packets.extend(dividers)
    packets.sort(key=cmp_to_key(compare))
    result = (packets.index(dividers[0]) + 1) * (packets.index(dividers[1]) + 1)
    return result
