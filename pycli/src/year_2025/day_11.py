from collections import defaultdict

import networkx as nx


def compute_path_count(graph, start, end):
    counts = defaultdict(int)
    counts[start] = 1
    for u in nx.topological_sort(graph):
        if u == end:
            return counts[end]

        for v in graph.successors(u):
            counts[v] += counts[u]

    raise ValueError(f"{end} not reached")


def part_1(text, example: bool = False):
    graph = nx.DiGraph()
    for line in text.splitlines():
        start, *ends = line.split()
        graph.add_edges_from([(start[:-1], end) for end in ends])

    return compute_path_count(graph, "you", "out")


def part_2(text, example: bool = False):

    graph = nx.DiGraph()
    for line in text.splitlines():
        start, *ends = line.split()
        graph.add_edges_from([(start[:-1], end) for end in ends])

    return (
        compute_path_count(graph, "svr", "fft")
        * compute_path_count(graph, "fft", "dac")
        * compute_path_count(graph, "dac", "out")
    )
