import sys
from itertools import product
from string import ascii_uppercase

import matplotlib.pyplot as plt
import networkx as nx
from pycli.src.grid import Grid


def dfs(grid, node, visited, found, counter=0):
    counter += 1
    value = str(grid[node])
    visited.add(node)

    is_empty = value == "."
    if not is_empty:
        found = found.copy()
        found.append(value)
        print(found)
        if len(found) >= 26:
            raise ValueError(f"finished in {counter} steps!")

        new_grid = Grid(grid.arr.copy())
        new_grid.replace(value, ".")
        new_grid.replace(value.upper(), ".")
        dfs(new_grid, node, set(), found, counter)

    neighbours = [
        neighbour
        for neighbour, _value in grid.neighbours(node)
        if (_value == "." or "a" <= _value <= "z") and neighbour not in visited
    ]

    for neighbour in neighbours:
        dfs(grid=grid, node=neighbour, visited=visited, found=found, counter=counter)

    return False


class Map:
    def __init__(self, grid):
        self.grid = grid
        self.start = self.grid.find("@")
        # self.grid.replace("@", ".")
        self.visited = set()
        self.dead_ends = set()
        self.graph = nx.DiGraph()

        self.first_dfs(self.start, None)

    def first_dfs(self, node, previous_letter):
        value = str(self.grid[node])
        self.visited.add(node)
        neighbours = [
            neighbour
            for neighbour, value in self.grid.neighbours(node)
            if value != "#" and neighbour not in self.visited
        ]
        is_empty = value == "."
        if not is_empty:
            if previous_letter:
                self.graph.add_edge(previous_letter, value)
            else:
                self.graph.add_node(value)
            previous_letter = value

        if not neighbours:
            if is_empty:
                self.dead_ends.add(node)

            return is_empty

        results = [
            self.first_dfs(neighbour, previous_letter) for neighbour in neighbours
        ]

        if all(results) and is_empty:
            self.dead_ends.add(node)
            return True

        else:
            return False


def simplify_graph(graph):
    while any(
        "A" <= (node := _node) <= "Z" and not graph[_node]
        for _node in list(graph.nodes())
    ):
        print(node)
        graph.remove_node(node)

    for node in list(graph.nodes()):
        if "A" <= node <= "Z" and node.lower() in nx.ancestors(graph, node):
            ancestors = list(graph.predecessors(node))
            successors = list(graph.successors(node))
            print(ancestors, successors)
            graph.add_edge(ancestors[0], successors[0])
            graph.remove_node(node)

    # while any("A" <= (node := _node) <= "Z" for _node in list(graph.nodes())):
    #     ancestors = list(graph.predecessors(node))
    #     successors = list(graph.successors(node))
    #     for ancestor, successor in product(ancestors, successors):
    #         graph.add_edge(ancestor, successor)
    #     for successor in successors:
    #         graph.add_edge(node.lower(), successor)
    #     graph.remove_node(node)


def part_1(text, example: bool = False):
    sys.setrecursionlimit(300_000)
    map_ = Map(Grid.from_text(text))
    for node in map_.dead_ends:
        if (node - map_.start).norm() > 2:
            map_.grid[node] = "#"

    simplify_graph(map_.graph)
    for node in set(ascii_uppercase) - set(map_.graph.nodes()):
        map_.grid.replace(node, ".")

    map_ = Map(map_.grid)
    for node in map_.dead_ends:
        if (node - map_.start).norm() > 2:
            map_.grid[node] = "#"

    breakpoint()

    # dfs(grid=map_.grid, node=map_.start, visited=set(), found=[])
    # map_.grid.print()
    result = None
    return result


def part_2(text, example: bool = False):
    result = None
    return result


def pretty_print_tree(G, root, level=0, prefix=""):
    """
    Recursively prints a tree in a pretty format.

    Parameters:
        G (nx.DiGraph): A directed graph representing the tree.
        root: The root node of the tree to start printing from.
        level (int): Current level in the tree for indentation.
        prefix (str): A prefix to customize branch symbols (e.g., └──, ├──).
    """
    indent = "  " * level
    connector = prefix if prefix else ""
    print(f"{indent}{connector}{root}")

    children = list(G.successors(root))
    for i, child in enumerate(children):
        # Use different branch symbols for the last child
        is_last = i == len(children) - 1
        new_prefix = "└── " if is_last else "├── "
        pretty_print_tree(G, child, level + 1, new_prefix)
