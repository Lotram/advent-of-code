import math
import re
from collections import defaultdict
from itertools import count

import networkx as nx


pattern = re.compile(r"\d+ \w+")


def parse_chemical(chemical):
    value, name = chemical.split()
    return int(value), name


def parse(text):
    reactions = {}
    graph = nx.DiGraph()
    for line in text.strip().splitlines():
        *inputs, (produced, result) = map(parse_chemical, pattern.findall(line))
        reactions[result] = (inputs, produced)
        for _, _input in inputs:
            graph.add_edge(_input, result)

    return reactions, graph


def solve(nodes, reactions, fuel_needed):
    result = 0
    needs = defaultdict(int)
    needs["FUEL"] = fuel_needed
    for node in nodes:
        needed = needs[node]
        if node == "ORE":
            result += needed
            continue

        inputs, produced = reactions[node]
        reaction_count = math.ceil(needed / produced)

        for _count, _input in inputs:
            needs[_input] += _count * reaction_count

    return result


def part_1(text, example: bool = False):
    reactions, graph = parse(text)
    nodes = nx.dfs_postorder_nodes(graph, "ORE")
    result = solve(nodes, reactions, fuel_needed=1)
    return result


def part_2(text, example: bool = False):
    reactions, graph = parse(text)
    nodes = list(nx.dfs_postorder_nodes(graph, "ORE"))
    trillion = 1000000000000
    value = solve(nodes, reactions, 1)
    value = trillion // value
    iterations = 0
    while True:
        ore_needed = solve(nodes, reactions, value)
        iterations += 1
        if ore_needed > trillion:
            print(iterations)
            return value - 1
        if (trillion / ore_needed) > 1.1:
            print(iterations, value, trillion / ore_needed)
            value = int(value * trillion / ore_needed)
        else:
            value += 1
