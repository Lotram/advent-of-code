from itertools import starmap

import numpy as np

from pycli.src.dijkstra import dijkstra
from pycli.src.grid import Grid, Vector
from pycli.src.held_karp import held_karp_bitmask


def stop_cond_func(nodes):
    visited = set()

    def stop_condition(current):
        if current in nodes:
            visited.add(current)
            return visited == nodes
        return False

    return stop_condition


def get_neighbour_func(grid: Grid):
    def get_neighbours(node: Vector):
        for neighbour, value in grid.neighbours(node):
            if value != "#":
                yield (neighbour, 1)

    return get_neighbours


def part_1(text, example: bool = False):
    grid = Grid(np.array(list(map(list, text.strip().split("\n")))))
    nodes = sorted(
        starmap(Vector, zip(*np.where(np.vectorize(lambda x: x.isdigit())(grid.arr)))),
        key=lambda node: int(grid[node]),
    )
    get_neighbours = get_neighbour_func(grid)

    distances = [[0] * len(nodes) for _ in range(len(nodes))]

    for idx, node in enumerate(nodes[:-1]):
        stop_cond = stop_cond_func(set(nodes[idx + 1 :]))
        dists_from_node = dijkstra(node, stop_cond, get_neighbours, return_all=True)
        for other_idx, other_node in enumerate(nodes[idx + 1 :], idx + 1):
            distances[idx][other_idx] = dists_from_node[other_node]
            distances[other_idx][idx] = dists_from_node[other_node]

    max_value = len(nodes) * max(distance for dists in distances for distance in dists)

    # add a node with a distance of 0 to the start, and max_value to_all other nodes
    distances_with_dummy = [
        [0, *[max_value] * (len(distances))],
        [0, *distances[0]],
        *[[max_value, *row] for row in distances[1:]],
    ]

    cost, path = held_karp_bitmask(distances_with_dummy)
    cost -= max_value

    # path = [idx - 1 for idx in path[1:]]
    # if path[0] != 0:
    #     path = path[::-1]

    return cost


def part_2(text, example: bool = False):
    grid = Grid(np.array(list(map(list, text.strip().split("\n")))))
    nodes = sorted(
        starmap(Vector, zip(*np.where(np.vectorize(lambda x: x.isdigit())(grid.arr)))),
        key=lambda node: int(grid[node]),
    )
    get_neighbours = get_neighbour_func(grid)

    distances = [[0] * len(nodes) for _ in range(len(nodes))]

    for idx, node in enumerate(nodes[:-1]):
        stop_cond = stop_cond_func(set(nodes[idx + 1 :]))
        dists_from_node = dijkstra(node, stop_cond, get_neighbours, return_all=True)
        for other_idx, other_node in enumerate(nodes[idx + 1 :], idx + 1):
            distances[idx][other_idx] = dists_from_node[other_node]
            distances[other_idx][idx] = dists_from_node[other_node]

    cost, path = held_karp_bitmask(distances)

    return cost
