import math
from collections import defaultdict


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    row_count = len(lines)
    col_count = len(lines[0])
    grid = {
        (row, col): int(char)
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
    }
    visible = set()
    for row in range(row_count):
        value = -1
        for col in range(col_count):
            if value < grid[row, col]:
                visible.add((row, col))
                value = grid[row, col]

        value = -1
        for col in range(col_count - 1, -1, -1):
            if value < grid[row, col]:
                visible.add((row, col))
                value = grid[row, col]

    for col in range(col_count):
        value = -1
        for row in range(row_count):
            if value < grid[row, col]:
                visible.add((row, col))
                value = grid[row, col]

        value = -1
        for row in range(row_count - 1, -1, -1):
            if value < grid[row, col]:
                visible.add((row, col))
                value = grid[row, col]

    return len(visible)


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    row_count = len(lines)
    col_count = len(lines[0])
    grid = {
        (row, col): int(char)
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
    }

    directions = ["up", "down", "left", "right"]
    limits = {dir: defaultdict(dict) for dir in directions}
    distances = defaultdict(list)
    for row in range(row_count):
        for col in range(col_count):
            tree = grid[row, col]
            distances[row, col].append(col - limits["left"][row].get(tree, 0))
            distances[row, col].append(row - limits["up"][col].get(tree, 0))
            for val in range(tree + 1):
                limits["left"][row][val] = col
                limits["up"][col][val] = row

            # use the same loop to compute other directions
            orow = row_count - row - 1
            ocol = col_count - col - 1
            otree = grid[orow, ocol]
            distances[orow, ocol].append(
                limits["right"][orow].get(otree, col_count - 1) - ocol
            )
            distances[orow, ocol].append(
                limits["down"][ocol].get(otree, row_count - 1) - orow
            )

            for val in range(otree + 1):
                limits["right"][orow][val] = ocol
                limits["down"][ocol][val] = orow

    return max(math.prod(val) for val in distances.values())
