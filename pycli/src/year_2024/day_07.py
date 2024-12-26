import re
from operator import sub, truediv


pattern = re.compile(r"\d+")


def parse(text):
    return [list(map(int, pattern.findall(line))) for line in text.strip().splitlines()]


def remove_suffix(value, number):
    return int(str(value).removesuffix(str(number)))


def backtrack(numbers, expected, ops):
    if expected != int(expected):
        return False

    if not numbers:
        return not expected

    if any(number > expected for number in numbers):
        return False

    expected = int(expected)

    for op in ops:
        if op == remove_suffix and not str(expected).endswith(str(numbers[-1])):
            continue

        if backtrack(numbers[:-1], op(expected, numbers[-1]), ops):
            return True

    return False


def solve(text, ops):
    return sum(
        expected
        for expected, *numbers in parse(text)
        if backtrack(numbers, expected, ops)
    )


def part_1(text, example: bool = False):
    return solve(text, [sub, truediv])


def part_2(text, example: bool = False):
    return solve(text, [sub, truediv, remove_suffix])
