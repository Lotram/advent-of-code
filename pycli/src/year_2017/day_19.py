import numpy as np

from .grid import DIRECTIONS, SOUTH, Grid


def solve(text):
    arr = np.array([list(line) for line in text.split("\n") if line])
    grid = Grid(arr)
    position = grid.find("|")
    direction = SOUTH
    letters = []
    steps = 0
    while (char := grid[position]) != " ":
        steps += 1
        if char.isalpha():
            letters.append(char)

        if char == "+":
            direction = next(
                dir_
                for dir_ in DIRECTIONS
                if dir_ != -direction and grid[position + dir_] != " "
            )

        position += direction
    return "".join(letters), steps


def part_1(text, example: bool = False):
    result, _ = solve(text)
    return result


def part_2(text, example: bool = False):
    _, result = solve(text)
    return result
