from collections import deque
from functools import cache
from itertools import chain, count

import networkx as nx


def build(numbers):
    numbers = numbers.copy()
    graph = nx.DiGraph()
    counter = count()

    def reduce(parent=None):
        child_count = numbers.popleft()
        metadata_count = numbers.popleft()
        node = next(counter)
        graph.add_node(node)

        for _ in range(child_count):
            reduce(parent=node)

        graph.nodes[node]["metadata"] = [
            numbers.popleft() for _ in range(metadata_count)
        ]
        if parent is not None:
            graph.add_edge(parent, node)

    reduce()
    return graph


def part_1(text, example: bool = False):
    numbers = deque(map(int, text.strip().split()))
    graph = build(numbers)

    result = sum(
        chain.from_iterable(
            node["metadata"] for node in dict(graph.nodes(data=True)).values()
        )
    )
    return result


def part_2(text, example: bool = False):
    numbers = deque(map(int, text.strip().split()))
    graph = build(numbers)

    @cache
    def get_value(node):
        metadata = graph.nodes[node]["metadata"]
        if successors := sorted(graph.successors(node)):
            return sum(
                get_value(successors[idx - 1])
                for idx in metadata
                if 1 <= idx <= len(successors)
            )

        else:
            return sum(graph.nodes[node]["metadata"])

    result = get_value(0)
    return result
