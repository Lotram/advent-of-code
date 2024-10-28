import heapq
from collections.abc import Callable, Iterable

from .grid import Grid, Vector


inf = float("inf")


def deprecated_heapq_dijkstra(graph, distances, start, end):
    min_dist = {node: 0 if node == start else inf for node in graph}
    prev = {node: None for node in graph}
    not_visited = []
    heapq.heappush(not_visited, (0, start))

    while not_visited:
        current = heapq.heappop(not_visited)[1]
        if current == end:
            break

        for neighbour, distance in distances[current].items():
            if min_dist[neighbour] > distance + min_dist[current]:
                min_dist[neighbour] = distance + min_dist[current]
                prev[neighbour] = current
                heapq.heappush(not_visited, (distance + min_dist[current], neighbour))

    def get_path(pre, node, path):
        if node is None:
            return path

        return get_path(pre, pre[node], [node, *path])

    return min_dist[end], get_path(prev, end, [])


def dijkstra(start, stop_condition, get_neighbours, return_all=False):
    return a_star(start, stop_condition, get_neighbours, return_all)


def a_star(start, stop_condition, get_neighbours, return_all=False, heuristic=None):
    if not callable(stop_condition):
        stop_condition = stop_condition.__eq__

    min_dist = {start: 0}
    prev = {start: None}
    not_visited = []
    heapq.heappush(not_visited, (0, start))
    while not_visited:
        current = heapq.heappop(not_visited)[1]
        if stop_condition(current):
            break

        for neighbour, distance in get_neighbours(current):
            if min_dist.get(neighbour, inf) > distance + min_dist[current]:
                min_dist[neighbour] = distance + min_dist[current]
                prev[neighbour] = current
                weight = min_dist[neighbour]
                if heuristic is not None:
                    weight += heuristic(neighbour)
                heapq.heappush(not_visited, (weight, neighbour))
    else:
        if return_all is False:
            raise ValueError("all nodes visited without finding a solution")

    def get_path(pre, node, path):
        if node is None:
            return path

        return get_path(pre, pre[node], [node, *path])

    if return_all:
        return min_dist

    return min_dist[current], get_path(prev, current, [])


def dijkstra_with_distance(distances, start, end):
    def get_neighbours(_, current):
        return distances[current].items()

    return dijkstra(start, end.__eq__, get_neighbours)


def matrix_dijkstra(
    grid: Grid,
    start: Vector,
    end: Vector,
    neighbour_function: Callable[[Grid, Vector], Iterable[tuple[Vector, int]]],
    initial_cost: int = 0,
):
    min_dist = {
        Vector(row, col): inf
        for row in range(grid.row_size)
        for col in range(grid.col_size)
    }
    min_dist[start] = initial_cost
    path = {node: [] for node in min_dist}

    not_visited = []
    heapq.heappush(not_visited, (0, start, []))

    while not_visited:
        current = heapq.heappop(not_visited)[1]
        if current == end:
            break

        for neighbour, distance in neighbour_function(grid, current):
            if min_dist[neighbour] > distance + min_dist[current]:
                min_dist[neighbour] = distance + min_dist[current]
                path[neighbour] = path[current] + [current]
                heapq.heappush(
                    not_visited, (min_dist[neighbour], neighbour, path[neighbour])
                )
    return min_dist[end], path[end] + [end]
