from itertools import chain, count, cycle, repeat
from math import sqrt

from .grid import DIAG_DIRECTIONS, EAST, NORTH, SOUTH, WEST, Point, Vector

DIRECTIONS = [EAST, NORTH, WEST, SOUTH]

ALL_DIRECTIONS = [*DIRECTIONS, *DIAG_DIRECTIONS]


def get_s_n(k):
    return Vector((k + 2) // 4 * pow(-1, k // 2), (k + 3) // 4 * pow(-1, (k + 3) // 2))


def get_value_s(n):
    value = 1 + 0.25 * (n + 1) ** 2
    if n % 2 == 0:
        value -= 0.25
    return int(value)


def get_n(value):
    # if n is odd, formula should be int(2 * sqrt(value - 1) - 1)
    return int(2 * sqrt(value - 3 / 4) - 1)


def part_1(text):
    value = int(text.strip())
    n = get_n(value)
    corner = get_s_n(n)
    position = corner + (value - get_value_s(n)) * DIRECTIONS[n % 4]

    result = int(position.norm())
    return result


def part_2(text):
    target = int(text.strip())
    data = {(point := Point(0, 0)): 1}
    dir_it = cycle(DIRECTIONS)
    length_it = (idx for i in count(1) for idx in chain(repeat(i, 2)))

    while True:
        direction = next(dir_it)
        length = next(length_it)
        idx = count()
        while next(idx) < length:
            point += direction
            data[point] = sum(
                data.get(point + direction, 0) for direction in ALL_DIRECTIONS
            )

            if data[point] > target:
                return data[point]
