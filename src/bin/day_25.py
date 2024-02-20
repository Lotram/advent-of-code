import math
from operator import methodcaller

from .karger_min_cut import Edge, Graph


def part_1(text):
    lines = text.strip().split("\n")
    vertices = set()
    edges = []
    for line in lines:
        start, others = line.split(": ")
        vertices.add(start)
        for other in map(methodcaller("strip"), others.split()):
            vertices.add(other)
            edges.append(Edge(src=start, dest=other))

    graph = Graph(vertices=vertices, edges=edges)
    while True:
        min_cut, ds_graph = graph.min_cut()
        if min_cut <= 3:
            ds = ds_graph.disjoint_set
            return math.prod(ds.elements[root].size for root in ds.roots)


def part_2(text):
    result = None
    return result
