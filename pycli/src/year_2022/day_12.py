from math import inf

from pycli.src.dijkstra import dijkstra
from pycli.src.grid import DIRECTIONS, Grid


def neighbours(grid, current):
    return [
        (neighbour, 1)
        for direction in DIRECTIONS
        if (neighbour := current + direction) in grid
        and ord(grid[neighbour]) >= ord(grid[current]) - 1
    ]


def part_1(text, example: bool = False):
    grid = Grid.from_text(text)
    start = grid.find("S")
    end = grid.find("E")
    grid[start] = "a"
    grid[end] = "z"

    def get_neighbours(current):
        return neighbours(grid, current)

    dist, _ = dijkstra(end, start.__eq__, get_neighbours=get_neighbours)
    return dist


def part_2(text, example: bool = False):
    grid = Grid.from_text(text)
    start = grid.find("S")
    end = grid.find("E")
    grid[start] = "a"
    grid[end] = "z"

    def get_neighbours(current):
        return neighbours(grid, current)

    distances = dijkstra(
        end, lambda x: False, get_neighbours=get_neighbours, return_all=True
    )
    candidates = grid.find_all("a")
    return min(distances.get(candidate, inf) for candidate in candidates)
