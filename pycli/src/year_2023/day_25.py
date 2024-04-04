from operator import methodcaller

from pycli.src.karger_min_cut import Edge, Graph


def part_1(text, example: bool = False):
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
        min_cut, size_1, size_2 = graph._min_cut()
        if min_cut == 3:
            return size_1 * size_2


def part_2(text, example: bool = False):
    result = None
    return result
