import heapq
from copy import deepcopy

import networkx as nx


def kahn(graph: nx.DiGraph):
    graph = deepcopy(graph)
    result = []

    available = [node for node, in_degree in graph.in_degree() if in_degree == 0]
    heapq.heapify(available)
    while available:
        node = heapq.heappop(available)
        result.append(node)
        for child in list(graph.successors(node)):
            graph.remove_edge(node, child)
            if not any(graph.predecessors(child)):
                heapq.heappush(available, child)

    return "".join(result)
