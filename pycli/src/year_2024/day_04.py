import numpy as np
from pycli.src.grid import Grid, Vector


letters = [(0, "X"), (1, "M"), (2, "A"), (3, "S")]


def _match(grid, position, direction):
    return all(
        (pos := position + idx * direction) in grid and grid[pos] == letter
        for idx, letter in letters
    )


def horizontal_match(grid, position):
    return _match(grid, position, Vector(0, 1))


def diagonal_match(grid, position):
    return _match(grid, position, Vector(1, 1))


def part_1(text, example: bool = False):
    arr = np.array([list(line) for line in text.strip().splitlines()])
    grid = Grid(arr)
    result = 0
    for _ in range(4):
        grid.rot90(1)
        result += sum(
            int(horizontal_match(grid, position)) + int(diagonal_match(grid, position))
            for position, _ in grid.flat_iter()
        )

    return result


letters_2 = [
    (Vector(0, 0), "A"),
    (Vector(-1, -1), "M"),
    (Vector(-1, 1), "M"),
    (Vector(1, -1), "S"),
    (Vector(1, 1), "S"),
]


def cross_match(grid, position):
    return all(
        (pos := position + direction) in grid and grid[pos] == letter
        for direction, letter in letters_2
    )


def part_2(text, example: bool = False):
    arr = np.array([list(line) for line in text.strip().splitlines()])
    grid = Grid(arr)
    result = 0
    for _ in range(4):
        grid.rot90(1)
        result += sum(
            int(cross_match(grid, position)) for position, _ in grid.flat_iter()
        )

    return result
