import re
from collections import defaultdict
from itertools import chain, combinations

import numpy as np
from pycli.src.dijkstra import dijkstra
from pycli.src.grid import EAST, NORTH, SOUTH, WEST, Grid, Vector


OFFSET = Vector(2, 2)


def build_portals(grid, text):
    letters = {
        Vector(row, col): char
        for row, line in enumerate(text.splitlines("\n"))
        for col, char in enumerate(line)
        if char.isalpha()
    }
    positions = list(reversed(letters))
    passages = defaultdict(list)
    while positions:
        first_position = positions.pop()
        passage_position, second_position = next(
            (passage_position, second_position)
            for (passage_direction, second_pos_direction) in {
                (2 * SOUTH, SOUTH),
                (2 * EAST, EAST),
                (NORTH, SOUTH),
                (WEST, EAST),
            }
            if grid.get(passage_position := first_position + passage_direction - OFFSET)
            and (second_position := first_position + second_pos_direction) in positions
        )
        positions.remove(second_position)
        passages[f"{letters[first_position]}{letters[second_position]}"].append(
            passage_position
        )
    return passages


def part_1(text, example: bool = False):
    grid = Grid(
        np.array(
            [
                [char == "." for char in line.strip().replace(" ", "#")]
                for line in re.sub("[A-Z]", " ", text).splitlines()
                if line.strip()
            ],
        )
    )
    portals = build_portals(grid, text)
    nodes = set(chain.from_iterable(portals.values()))
    AA = portals.pop("AA")[0]
    ZZ = portals.pop("ZZ")[0]

    distances = build_distances(grid, nodes)

    for _start, _end in portals.values():
        distances[_start][_end] = 1
        distances[_end][_start] = 1

    return dijkstra(AA, ZZ.__eq__, lambda current: distances[current].items())[0]


def build_distances(grid, nodes):
    def neighbour_function(current):
        neighbours = [
            _neighbour
            for direction in {NORTH, SOUTH, EAST, WEST}
            if grid.get(_neighbour := current + direction)
        ]

        return [(_neighbour, 1) for _neighbour in neighbours]

    to_do = nodes.copy()
    distances = defaultdict(dict)
    while to_do:
        item = to_do.pop()
        result = dijkstra(item, lambda _: False, neighbour_function, return_all=True)
        reachable = set(result) & to_do
        for node in reachable:
            distances[node][item] = result[node]
            distances[item][node] = result[node]

        for start, end in combinations(reachable, 2):
            _distance = dijkstra(start, end.__eq__, neighbour_function)[0]
            distances[start][end] = _distance
            distances[end][start] = _distance

        to_do -= reachable

    return distances


def part_2(text, example: bool = False):
    grid = Grid(
        np.array(
            [
                [char == "." for char in line.strip().replace(" ", "#")]
                for line in re.sub("[A-Z]", " ", text).splitlines()
                if line.strip()
            ],
        )
    )
    portals = build_portals(grid, text)
    nodes = set(chain.from_iterable(portals.values()))
    AA = portals.pop("AA")[0]
    ZZ = portals.pop("ZZ")[0]

    distances = build_distances(grid, nodes)
    pairs = {k: v for a, b in portals.values() for k, v in ((a, b), (b, a))}

    def get_neighbours(current):
        vec, layer = current
        neighbours = [
            ((neighbour, layer), distance)
            for neighbour, distance in distances[vec].items()
        ]
        if vec not in {AA, ZZ}:
            if vec.col in {0, grid.col_size - 1} or vec.row in {0, grid.row_size - 1}:
                new_layer = layer - 1
            else:
                new_layer = layer + 1
            if new_layer >= 0:
                neighbours = [*neighbours, ((pairs[vec], new_layer), 1)]

        return neighbours

    return dijkstra((AA, 0), (ZZ, 0).__eq__, get_neighbours)[0]
