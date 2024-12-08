import re
from itertools import product
from operator import add, mul


pattern = re.compile(r"\d+")


# like reduce, but with an iterator on the functions as well and return a boolean
def reduce(function_iterable, iterable, expected):
    it = iter(iterable)

    value = next(it)
    for function, element in zip(function_iterable, it):
        value = function(value, element)
        if value > expected:
            return False
    return value == expected


def parse(text):
    return [list(map(int, pattern.findall(line))) for line in text.strip().splitlines()]


def concat(a, b):
    return int(str(a) + str(b))


def part_1(text, example: bool = False):
    return sum(
        expected
        for expected, *numbers in parse(text)
        if any(
            reduce(op_combination, numbers, expected)
            for op_combination in product([add, mul], repeat=len(numbers) - 1)
        )
    )


# TODO That's obviously a suboptimal algorithm, find something better than dumb bruteforcing
def part_2(text, example: bool = False):
    return sum(
        expected
        for expected, *numbers in parse(text)
        if any(
            reduce(op_combination, numbers, expected)
            for op_combination in product([add, mul, concat], repeat=len(numbers) - 1)
        )
    )
