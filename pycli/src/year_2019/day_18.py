import math
import string
from string import ascii_uppercase

import networkx as nx
from pycli.src.grid import DIAG_DIRECTIONS, DIRECTIONS, Grid
from pycli.src.held_karp import held_karp
from pycli.src.print_tree import print_nx_tree


class Map:
    def __init__(self, grid, part):
        self.grid = grid
        self.start = self.grid.find("@")
        # self.grid.replace("@", ".")
        self.visited = set()
        self.dead_ends = set()
        self.tree = nx.DiGraph()
        self.distance_graph = nx.Graph()
        self.part = part

    def process(self):
        self.visited = {self.start + _direction for _direction in DIRECTIONS}
        for idx, diag_1 in enumerate(DIAG_DIRECTIONS):
            start = self.start + diag_1
            node = str(idx)
            self.grid[start] = node
            self.build_tree(start, "@")

        self.visited = set()
        self.remove_dead_ends()
        self.simplify_tree()

    def build_tree(self, node, previous_letter):
        value = str(self.grid[node])
        self.visited.add(node)
        neighbours = [
            neighbour
            for neighbour, value in self.grid.neighbours(node)
            if value != "#" and neighbour not in self.visited
        ]
        is_empty = value == "."
        if not is_empty:
            self.tree.add_node(value)
            if previous_letter:
                self.tree.add_edge(previous_letter, value)
            previous_letter = value

        if not neighbours:
            if is_empty:
                self.dead_ends.add(node)

            return is_empty

        results = [
            self.build_tree(neighbour, previous_letter) for neighbour in neighbours
        ]

        if all(results) and is_empty:
            self.dead_ends.add(node)
            return True

        else:
            return False

    def simplify_tree(self):
        # if an upper letter does not have any children, remove it
        while any(
            (node := _node).isupper() and not self.tree[_node]
            for _node in list(self.tree.nodes())
        ):
            self.tree.remove_node(node)

        for node in list(self.tree.nodes()):
            if node.isupper() and node.lower() in nx.ancestors(self.tree, node):
                ancestors = list(self.tree.predecessors(node))
                successors = list(self.tree.successors(node))
                self.tree.add_edge(ancestors[0], successors[0])
                self.tree.remove_node(node)

        # remove those from the grid
        for node in set(ascii_uppercase) - set(self.tree.nodes()):
            self.grid.replace(node, ".")

        # if an upper case appears after lower, remove it
        while any(
            (
                (node := _node).islower()
                and len(list(self.tree.successors(node)))
                and node.upper() not in self.tree.nodes
            )
            for _node in list(self.tree.nodes())
        ):
            ancestor = list(self.tree.predecessors(node))[0]
            successors = list(self.tree.successors(node))
            for successor in successors:
                self.tree.add_edge(ancestor, successor)
            self.grid.replace(node, ".")
            self.tree.remove_node(node)

        self.remove_dead_ends()

    def build_precedence_graph(self):
        self.precedence_graph = nx.DiGraph()
        for node in self.tree:
            if node.isupper():
                continue
            self.precedence_graph.add_node(node)
            for ancestor in nx.ancestors(self.tree, node):
                if ancestor.isupper() or ancestor.islower():
                    self.precedence_graph.add_edge(ancestor.lower(), node)

        # Add more constraints, not necessary, but apparently faster
        for node in self.precedence_graph:
            for ancestor in nx.ancestors(self.precedence_graph, node):
                self.precedence_graph.add_edge(ancestor, node)

    def dfs(self, node, previous_node, dist=0):
        value = str(self.grid[node])
        self.visited.add(node)
        neighbours = [
            neighbour
            for neighbour, value in self.grid.neighbours(node)
            if value != "#" and neighbour not in self.visited
        ]

        if len(neighbours) > 1 or (value != "." and not value.isupper()):
            new_node = value if value != "." else node
            self.distance_graph.add_node(new_node)
            if previous_node:
                self.distance_graph.add_edge(previous_node, new_node, weight=dist)
            dist = 0
            previous_node = new_node

        for neighbour in neighbours:
            self.dfs(neighbour, previous_node, dist + 1)

    def get_distances(self):
        self.visited = {self.start + _direction for _direction in DIRECTIONS}

        for node in ("0", "1", "2", "3"):
            if self.part == 1:
                self.distance_graph.add_edge(node, str((int(node) + 1) % 4), weight=2)
                self.dfs(self.grid.find(node), "@", 2)
            else:
                self.dfs(self.grid.find(node), None)

    def remove_dead_ends(self):
        for node in self.dead_ends:
            if (node - self.start).norm() > 2:
                self.grid[node] = "#"

    def remove_doors(self):
        while any((node := _node).isupper() for _node in list(self.tree.nodes())):
            predecessors = list(self.tree.predecessors(node))[0]
            successors = list(self.tree.successors(node))
            for successor in successors:
                self.tree.add_edge(predecessors, successor)
            self.tree.remove_node(node)
            self.grid.replace(node, ".")

    def print_grid(self):
        color_rules = (
            dict.fromkeys(string.ascii_lowercase, "green3")
            | dict.fromkeys(string.ascii_uppercase, "red")
            | {".": "yellow", "#": "grey39"}
        )

        self.grid.print(color_rules=color_rules)

    def print_tree(self):
        print_nx_tree(self.tree, "@")

    def print_distance_graph(self):
        print_nx_tree(
            self.distance_graph,
            "@",
            node_str=lambda node: "*" if str(node).startswith("Vector") else str(node),
        )


def part_1(text, example: bool = False):
    if example:
        raise NotImplementedError("this does not work for the example values")
    map_ = Map(Grid.from_text(text), part=1)
    map_.process()

    map_.build_precedence_graph()
    map_.get_distances()

    all_distances = dict(nx.all_pairs_dijkstra_path_length(map_.distance_graph))
    nodes = sorted(node for node in map_.tree.nodes if node.islower() or node == "@")
    distances = [[all_distances[node][_node] for _node in nodes] for node in nodes]

    # We want TSP path, no cycle
    # so we create a sink to force this
    distances = [
        *[[*row, 0] for idx, row in enumerate(distances)],
        [0, *[math.inf] * len(distances)],
    ]

    idx_by_node = {value: idx for idx, value in enumerate(nodes)}

    predecessors_by_idx = {
        idx_by_node[node]: {idx_by_node[pred] for pred in preds}
        for node in nodes
        if (preds := list(map_.precedence_graph.predecessors(node)))
    }
    length, path = held_karp(distances, predecessors=predecessors_by_idx)
    # path_nodes = [nodes[idx] for idx in path[:-1]]
    result = length
    return result


def part_2(text, example: bool = False):
    result = 0
    map_ = Map(Grid.from_text(text), part=2)

    map_.process()

    map_.build_precedence_graph()
    map_.get_distances()

    all_distances = dict(nx.all_pairs_dijkstra_path_length(map_.distance_graph))

    all_nodes = sorted(
        node for node in map_.tree.nodes if node.islower() or node.isdigit()
    )
    for start in ("0", "1", "2", "3"):
        nodes = sorted(node for node in all_nodes if node in all_distances[start])
        distances = [[all_distances[node][_node] for _node in nodes] for node in nodes]

        # We want TSP path, no cycle
        # so we create a sink to force this
        distances = [
            *[[*row, 0] for idx, row in enumerate(distances)],
            [0, *[math.inf] * len(distances)],
        ]

        idx_by_node = {value: idx for idx, value in enumerate(nodes)}

        predecessors_by_idx = {
            idx_by_node[node]: {idx_by_node[pred] for pred in preds if pred in nodes}
            for node in nodes
            if (preds := list(map_.precedence_graph.predecessors(node)))
        }
        length, path = held_karp(distances, predecessors=predecessors_by_idx)
        # path_nodes = [nodes[idx] for idx in path[:-1]]
        result += length
    return result
