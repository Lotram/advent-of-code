from collections.abc import Iterator
from typing import NamedTuple

import numpy as np

from .dijkstra import dijkstra
from .grid import DIRECTIONS, EAST, Grid, Point, Vector

inf = float("inf")

DIRECTION_SET = set(DIRECTIONS)


class Node(NamedTuple):
    point: Point
    direction: Vector
    count: int


def get_neighbours_func(grid: Grid):
    def get_neighbours(node: Node) -> Iterator[tuple[Node, int]]:
        point, direction, count = node
        other_directions = DIRECTION_SET - {direction, -direction}

        neighbours = []
        for other_direction in other_directions:
            neighbours.append(Node(point + other_direction, other_direction, 1))
        if count < 3:
            neighbours.append(Node(point + direction, direction, count + 1))

        for neighbour in neighbours:
            if neighbour.point in grid:
                yield (neighbour, grid[neighbour.point])

    return get_neighbours


def stop_condition_func(end_point):
    def stop_condition(node: Node) -> bool:
        return node.point == end_point

    return stop_condition


def solution(grid, get_neighbours):
    start = Node(Point(0, 0), EAST, 0)
    end_point = Point(grid.row_size - 1, grid.col_size - 1)
    stop_condition = stop_condition_func(end_point)
    result = dijkstra(start, stop_condition, get_neighbours)
    return result[0]


def part_1(text):
    arr = np.array(tuple(tuple(map(int, line)) for line in text.strip().split("\n")))
    grid = Grid(arr)
    get_neighbours = get_neighbours_func(grid)
    start = Node(Point(0, 0), EAST, 0)
    end_point = Point(grid.row_size - 1, grid.col_size - 1)
    stop_condition = stop_condition_func(end_point)
    result = dijkstra(start, stop_condition, get_neighbours)
    return result[0]


def get_neighbours_func_2(grid: Grid):
    def get_neighbours(node: Node) -> Iterator[tuple[Node, int]]:
        point, direction, count = node
        other_directions = DIRECTION_SET - {direction, -direction}

        neighbours = []
        if count == 0 or count >= 4:
            for other_direction in other_directions:
                neighbours.append(Node(point + other_direction, other_direction, 1))
        if count < 10:
            neighbours.append(Node(point + direction, direction, count + 1))

        for neighbour in neighbours:
            if neighbour.point in grid:
                yield (neighbour, grid[neighbour.point])

    return get_neighbours


def stop_condition_func_2(end_point):
    def stop_condition(node: Node) -> bool:
        return node.point == end_point and node.count >= 4

    return stop_condition


def part_2(text):
    arr = np.array(tuple(tuple(map(int, line)) for line in text.strip().split("\n")))
    grid = Grid(arr)
    get_neighbours = get_neighbours_func_2(grid)
    start = Node(Point(0, 0), EAST, 0)
    end_point = Point(grid.row_size - 1, grid.col_size - 1)
    stop_condition = stop_condition_func_2(end_point)
    result = dijkstra(start, stop_condition, get_neighbours)
    return result[0]
