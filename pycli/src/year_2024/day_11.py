import sys
from functools import cache


@cache
def _get_stones(value):
    if value == 0:
        return (1,)

    if (length := len(digits := str(value))) % 2 == 0:
        return (int(digits[: length // 2]), int(digits[length // 2 :]))

    return (value * 2024,)


def get_all_stones(values):
    return [_stone for stone in values for _stone in _get_stones(stone)]


@cache
def get_result(stone, iterations):
    if iterations == 0:
        return 1

    return sum(get_result(_stone, iterations - 1) for _stone in _get_stones(stone))


def part_1(text, example: bool = False):
    stones = list(map(int, text.strip().split()))
    ITERATIONS = 25
    result = sum(get_result(stone, ITERATIONS) for stone in stones)
    return result


def part_2(text, example: bool = False):
    stones = list(map(int, text.strip().split()))
    ITERATIONS = 75
    result = sum(get_result(stone, ITERATIONS) for stone in stones)
    return result
