import heapq
import re

import networkx as nx

from pycli.src.topological_sort import kahn

pattern = re.compile(r"[A-Z](?=\ )")


def part_1(text, example: bool = False):
    graph = nx.DiGraph(pattern.findall(line) for line in text.strip().split("\n"))
    result = kahn(graph)
    return result


def part_2(text, example: bool = False):
    graph = nx.DiGraph(pattern.findall(line) for line in text.strip().split("\n"))

    def duration(node):
        return 60 * (1 - example) + ord(node) + 1 - ord("A")

    worker_count = 2 if example else 5

    waiting = [node for node, in_degree in graph.in_degree() if in_degree == 0]
    heapq.heapify(waiting)

    running = [(None, None)] * worker_count
    prev_t = t = 0
    while graph.edges or waiting:
        # handle finished tasks
        if prev_t < t:
            for idx, (node, end_at) in enumerate(running):
                if end_at is not None and end_at <= t:
                    running[idx] = (None, None)
                    for child in list(graph.successors(node)):
                        graph.remove_edge(node, child)
                        if not any(graph.predecessors(child)):
                            heapq.heappush(waiting, child)

            prev_t = t

        # if a task is waiting, start it
        if waiting:
            node = heapq.heappop(waiting)
            worker_idx = next(
                idx for idx, worker in enumerate(running) if worker == (None, None)
            )
            running[worker_idx] = (node, t + duration(node))

        # some tasks are waiting, and workers are available
        if not (any(worker == (None, None) for worker in running) and waiting):
            t = min(end_at for (_, end_at) in running if end_at is not None)

    result = t
    return result
