import math
import re
from collections import defaultdict

import networkx as nx


pattern = re.compile(r"\d+ \w+")


def parse_chemical(chemical):
    value, name = chemical.split()
    return int(value), name


def parse(text):
    reactions = {}
    graph = nx.DiGraph()
    for line in text.strip().splitlines():
        *inputs, (result_count, result) = map(parse_chemical, pattern.findall(line))
        reactions[result] = (inputs, result_count)
        for _, _input in inputs:
            graph.add_edge(_input, result)

    return reactions, graph


def part_1(text, example: bool = False):
    reactions, graph = parse(text)
    result = 0
    needs = defaultdict(int)
    needs["FUEL"] = 1
    nodes = nx.dfs_postorder_nodes(graph, "ORE")
    for node in nodes:
        needed = needs[node]
        if node == "ORE":
            result += needed
            continue

        inputs, result_count = reactions[node]
        reaction_count = math.ceil(needed / result_count)

        for count, _input in inputs:
            needs[_input] += count * reaction_count

    return result


def part_2(text, example: bool = False):
    result = None
    return result
