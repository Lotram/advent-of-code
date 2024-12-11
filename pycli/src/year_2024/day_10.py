import numpy as np
from pycli.src.grid import Grid


def get_next(grid, value, position):
    if value == 9:
        yield position
    for _position, _value in grid.neighbours(position):
        if _value == value + 1:
            yield from get_next(grid, _value, _position)


def part_1(text, example: bool = False):
    grid = Grid(np.array([list(map(int, line)) for line in text.strip().splitlines()]))
    starts = grid.find_all(0)
    result = 0
    for start in starts:
        result += len(set(get_next(grid, 0, start)))
    return result


def part_2(text, example: bool = False):
    grid = Grid(np.array([list(map(int, line)) for line in text.strip().splitlines()]))
    starts = grid.find_all(0)
    result = 0
    for start in starts:
        result += len(list(get_next(grid, 0, start)))
    return result
