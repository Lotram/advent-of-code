from itertools import dropwhile, takewhile

import networkx


def build_graph(text):
    graph = networkx.Graph()
    for edge in text.strip().splitlines():
        graph.add_edge(*edge.split("-"))

    return graph


def list_all_cliques(graph, size=3):
    all_cliques = networkx.enumerate_all_cliques(graph)
    predicate_false = lambda clique: len(clique) != size
    predicate_true = lambda clique: len(clique) == size
    start_with_t = lambda nodes: any(node[0] == "t" for node in nodes)
    cliques = takewhile(predicate_true, dropwhile(predicate_false, all_cliques))
    cliques_with_t = filter(start_with_t, cliques)
    return list(cliques_with_t)


def part_1(text, example: bool = False):
    graph = build_graph(text)
    result = len(list_all_cliques(graph))

    return result


def part_2(text, example: bool = False):
    graph = build_graph(text)
    largest_clique = []
    for clique in networkx.find_cliques(graph):
        if len(clique) > len(largest_clique):
            largest_clique = clique
    result = ",".join(sorted(largest_clique))
    return result
