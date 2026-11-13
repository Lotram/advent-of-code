import heapq


inf = float("inf")


def dijkstra(start, stop_condition, get_neighbours, return_all=False):
    return a_star(start, stop_condition, get_neighbours, return_all)


def a_star(start, stop_condition, get_neighbours, return_all=False, heuristic=None):
    if not callable(stop_condition):
        stop_condition = stop_condition.__eq__

    min_dist = {start: 0}
    prev = {start: None}
    not_visited = []
    heapq.heappush(not_visited, (0, id(start), start))
    while not_visited:
        current = heapq.heappop(not_visited)[-1]
        if stop_condition(current):
            break

        for neighbour, distance in get_neighbours(current):
            if min_dist.get(neighbour, inf) > distance + min_dist[current]:
                min_dist[neighbour] = distance + min_dist[current]
                prev[neighbour] = current
                weight = min_dist[neighbour]
                if heuristic is not None:
                    weight += heuristic(neighbour)
                heapq.heappush(not_visited, (weight, id(neighbour), neighbour))
    else:
        if return_all is False:
            return inf, []

    if return_all:
        return min_dist

    def get_path(node, path):
        if node is None:
            return path

        return get_path(prev[node], [node, *path])

    return min_dist[current], get_path(current, [])
