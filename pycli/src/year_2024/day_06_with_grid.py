import numpy as np
from pycli.src.grid import DIRECTIONS, Grid


def get_visited(grid, start):
    direction = DIRECTIONS[0]
    obstructions = set(grid.find_all("#"))
    visited = set()
    position = start
    while position in grid:
        visited.add(position)
        position += direction
        while position + direction in obstructions:
            direction = direction.rotate(1)

    return visited


def part_1(text, example: bool = False):
    array = np.array([list(line) for line in text.strip().splitlines()])
    grid = Grid(arr=array)
    start = grid.find("^")
    visited = get_visited(grid, start)
    result = len(visited)
    return result


def part_2(text, example: bool = False):
    array = np.array([list(line) for line in text.strip().splitlines()])
    grid = Grid(arr=array)
    result = 0
    obstructions = set(grid.find_all("#"))
    start = grid.find("^")
    visited_positions = get_visited(grid, start)

    for candidate in visited_positions - {start}:
        _obstructions = obstructions | {candidate}
        position = start
        direction = DIRECTIONS[0]
        visited = set()
        while position in grid:
            if (position, direction) in visited:
                result += 1
                break

            visited.add((position, direction))
            position += direction
            while position + direction in _obstructions:
                direction = direction.rotate(1)

    return result
