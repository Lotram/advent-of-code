import re
from collections import defaultdict, deque

pattern = re.compile(r"\d+")


def build_graph(text):
    graph = defaultdict(set)
    for line in text.strip().split("\n"):
        node, *neighbours = pattern.findall(line)
        graph.setdefault(node, set())
        for neighbour in neighbours:
            if neighbour != node:
                graph[node].add(neighbour)
                graph[neighbour].add(node)
    return graph


def find_subgraph(graph, start):
    visited = set()
    queue = deque([start])
    while queue:
        current = queue.popleft()
        visited.add(current)
        for neighbour in graph[current]:
            if neighbour not in visited:
                queue.append(neighbour)

    return visited


def part_1(text, example: bool = False):
    graph = build_graph(text)
    visited = find_subgraph(graph, "0")
    result = len(visited)
    return result


def part_2(text, example: bool = False):
    graph = build_graph(text)
    result = 0
    remaining_nodes = set(graph)
    while remaining_nodes:
        start = remaining_nodes.pop()
        remaining_nodes -= find_subgraph(graph, start)
        result += 1
    return result
