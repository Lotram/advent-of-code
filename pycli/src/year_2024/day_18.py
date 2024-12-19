from functools import partial

import numpy as np
from pycli.src.dijkstra import dijkstra
from pycli.src.grid import Grid, Vector


def parse(text, size, bytes_to_consider):
    grid = Grid(np.full((size + 1, size + 1), False, dtype="bool"))
    bytes = [tuple(map(int, line.split(","))) for line in text.strip().splitlines()]
    for x, y in bytes[:bytes_to_consider]:
        grid[Vector(y, x)] = True

    return grid


def get_neighbours(grid, position):
    for neighbour, value in grid.neighbours(position):
        if not value:
            yield (neighbour, 1)


def part_1(text, example: bool = False):
    size = 6 if example else 70
    bytes_to_consider = 12 if example else 1024
    start = Vector(0, 0)
    end = Vector(size, size)
    grid = parse(text, size, bytes_to_consider)
    result, _ = dijkstra(start, end.__eq__, partial(get_neighbours, grid))
    return result


def find_boundary(f, low, high):
    """
    Find the smallest integer where the function f changes from False to True.

    :param f: A function that takes an int and returns a boolean (True/False).
    :param low: The lower bound of the search range.
    :param high: The upper bound of the search range.
    :return: The integer where f changes from False to True.
    """
    while low < high:
        mid = (low + high) // 2
        if f(mid):  # If True, search the lower half
            high = mid
        else:  # If False, search the upper half
            low = mid + 1
    return low


def func(start, end, grid):
    try:
        dijkstra(start, end.__eq__, partial(get_neighbours, grid))
    except ValueError:
        return False
    else:
        return True


def part_2(text, example: bool = False):
    low = 12 if example else 1024

    size = 6 if example else 70
    high = len(text.strip().splitlines())
    start = Vector(0, 0)
    end = Vector(size, size)
    while low < high:
        mid = (low + high) // 2
        grid = parse(text, size, mid)
        if func(start, end, grid):
            low = mid + 1
        else:
            high = mid

    result = text.strip().splitlines()[low - 1]

    return result
