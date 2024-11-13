import networkx


def count_connected_subgraphs(graph):
    visited = set()
    count = 0

    for node in graph:
        if node not in visited:
            dfs(graph, node, visited)
            count += 1

    return count


def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)


def distance(node, other):
    return sum(abs(node[i] - other[i]) for i in range(4))


def part_1(text, example: bool = False):
    graph = networkx.Graph()
    nodes = [tuple(map(int, line.split(","))) for line in text.strip().splitlines()]
    for i in range(len(nodes)):
        graph.add_node(i)
        for j in range(i + 1, len(nodes)):
            if distance(nodes[i], nodes[j]) <= 3:
                graph.add_edge(i, j)
    result = count_connected_subgraphs(graph)
    # result = networkx.number_connected_components(graph)
    return result


def part_2(text, example: bool = False):
    result = None
    return result
