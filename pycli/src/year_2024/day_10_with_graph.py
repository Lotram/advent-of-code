from itertools import product

import networkx as nx
import numpy as np
from pycli.src.grid import Grid


def part_1(text, example: bool = False):
    graph = nx.DiGraph()
    grid = Grid(np.array([list(map(int, line)) for line in text.strip().splitlines()]))
    starts = set()
    ends = set()
    for position, value in grid.flat_iter():
        for neighbour_position, neighbour_value in grid.neighbours(position):
            if neighbour_value == value + 1:
                graph.add_edge(position, neighbour_position)

            if value == 0:
                starts.add(position)
            if value == 9:
                ends.add(position)

    result = sum(
        1 for start, end in product(starts, ends) if nx.has_path(graph, start, end)
    )
    return result


def part_2(text, example: bool = False):
    graph = nx.DiGraph()
    grid = Grid(np.array([list(map(int, line)) for line in text.strip().splitlines()]))
    starts = set()
    ends = set()
    for position, value in grid.flat_iter():
        for neighbour_position, neighbour_value in grid.neighbours(position):
            if neighbour_value == value + 1:
                graph.add_edge(position, neighbour_position)

            if value == 0:
                starts.add(position)
            if value == 9:
                ends.add(position)

    result = sum(
        len(list(nx.all_shortest_paths(graph, start, end)))
        for start, end in product(starts, ends)
        if nx.has_path(graph, start, end)
    )
    return result
