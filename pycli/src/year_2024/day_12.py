from collections import deque
from itertools import pairwise

from pycli.src.grid import EAST, NORTH, SOUTH, WEST, Grid, Vector


def part_1(text, example: bool = False):
    grid = Grid.from_text(text)
    to_visit = set(grid.flat_iter())
    result = 0
    while to_visit:
        _position, value = to_visit.pop()
        _to_visit = {_position}
        visited = set()
        area = 0
        perimeter = 0
        while _to_visit:
            position = _to_visit.pop()
            visited.add(position)
            area += 1
            neighbours = list(grid.neighbours(position))
            for n_position, n_value in neighbours:
                if value == n_value:
                    if n_position not in visited:
                        _to_visit.add(n_position)
                else:
                    perimeter += 1

            perimeter += 4 - len(neighbours)

        to_visit -= {(_visited, value) for _visited in visited}
        result += perimeter * area

    return result


directions = [NORTH, EAST, SOUTH, WEST]
angles = [(NORTH, EAST), (EAST, SOUTH), (SOUTH, WEST), (WEST, NORTH)]


def part_2(text, example: bool = False):
    grid = Grid.from_text(text)
    to_visit = set(grid.flat_iter())
    result = 0
    while to_visit:
        _position, value = to_visit.pop()
        _to_visit = {_position}
        visited = set()
        area = 0
        corners = 0
        while _to_visit:
            position = _to_visit.pop()
            visited.add(position)
            area += 1
            values = {}
            for direction in directions:
                n_position = position + direction
                n_value = grid.get(n_position) == value
                values[direction] = n_value
                if n_value and n_position not in visited:
                    _to_visit.add(n_position)

            for dir1, dir2 in angles:
                val1 = values[dir1]
                val2 = values[dir2]
                if val1 and val2:
                    corners += grid.get(position + dir1 + dir2) != value

                if not (val1 or val2):
                    corners += 1

        to_visit -= {(_visited, value) for _visited in visited}
        result += corners * area
    return result
