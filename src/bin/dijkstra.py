import heapq

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


def dijkstra(start, end, get_neighbours):
    return a_star(start, end, get_neighbours, lambda node: 0)


def a_star(start, end, get_neighbours, heuristic):
    min_dist = {start: 0}
    prev = {start: None}
    not_visited = []
    heapq.heappush(not_visited, (0, start))
    count = 0
    n_count = 0
    while not_visited:
        count += 1
        current = heapq.heappop(not_visited)[1]
        if current == end:
            break

        for neighbour, distance in get_neighbours(current):
            n_count += 1
            if min_dist.get(neighbour, inf) > distance + min_dist[current]:
                min_dist[neighbour] = distance + min_dist[current]
                prev[neighbour] = current
                heapq.heappush(
                    not_visited, (min_dist[neighbour] + heuristic(neighbour), neighbour)
                )

    def get_path(pre, node, path):
        if node is None:
            return path

        return get_path(pre, pre[node], [node, *path])

    print("count", count)
    print("n_count", n_count)
    return min_dist[end], get_path(prev, end, [])


def dijkstra_with_distance(distances, start, end):
    def get_neighbours(_, current):
        return distances[current].items()

    return dijkstra(start, end, get_neighbours)


def neighbours(grid, row, col):
    _neighbours = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]
    return [
        ((_row, _column), grid[_row][_column])
        for _row, _column in _neighbours
        if 0 <= _row < len(grid) and 0 <= _column < len(grid[0])
    ]


def matrix_dijkstra(grid, start, end, neighbour_function):
    min_dist = {
        (row, col): inf for row in range(len(grid)) for col in range(len(grid[0]))
    }
    min_dist[start] = grid[start[0]][start[1]]
    path = {node: [] for node in min_dist}

    not_visited = []
    heapq.heappush(not_visited, (0, start, []))

    while not_visited:
        current = heapq.heappop(not_visited)[1]
        if current == end:
            break

        for neighbour, distance in neighbour_function(grid, *current):
            if min_dist[neighbour] > distance + min_dist[current]:
                min_dist[neighbour] = distance + min_dist[current]
                path[neighbour] = path[current] + [current]
                heapq.heappush(
                    not_visited, (min_dist[neighbour], neighbour, path[neighbour])
                )

    return min_dist[end], path[end] + [end]
