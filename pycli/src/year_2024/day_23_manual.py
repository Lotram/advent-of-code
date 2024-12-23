from collections import defaultdict

from pycli.src.bron_kerbosch import BronKerbosh


# TODO
def part_1(text, example: bool = False):
    result = 0

    return result


def build_graph(text):
    graph = defaultdict(set)
    for edge in text.strip().splitlines():
        u, v = edge.split("-")
        graph[u].add(v)
        graph[v].add(u)

    return graph


def part_2(text, example: bool = False):
    graph = build_graph(text)
    cliques = BronKerbosh(graph).run(version=2)
    result = ",".join(sorted(max(cliques, key=len)))

    return result
