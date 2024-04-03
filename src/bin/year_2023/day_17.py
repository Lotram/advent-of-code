import heapq

inf = float("inf")


def get_neighbours(node):
    row, col, direction, count = node
    other_directions = {(0, 1), (0, -1), (1, 0), (-1, 0)} - {
        direction,
        (-direction[0], -direction[1]),
    }

    for other_direction in other_directions:
        yield (row + other_direction[0], col + other_direction[1], other_direction, 1)

    if count < 3:
        yield (row + direction[0], col + direction[1], direction, count + 1)


def matrix_dijkstra(grid, start_position, end):
    start = (*start_position, (0, 1), 0)
    min_dist = {start: 0}
    path = {start: [start]}

    not_visited = []
    heapq.heappush(not_visited, (0, start, []))

    while not_visited:
        current = heapq.heappop(not_visited)[1]
        if (current[0], current[1]) == end:
            end_node = current
            break

        for neighbour in get_neighbours(current):
            row, col, _, _ = neighbour
            if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
                continue

            distance = grid[row][col]
            if min_dist.get(neighbour, inf) > distance + min_dist[current]:
                min_dist[neighbour] = distance + min_dist[current]
                path[neighbour] = path[current] + [current]
                heapq.heappush(
                    not_visited, (min_dist[neighbour], neighbour, path[neighbour])
                )

    return min_dist[end_node], path[end_node] + [end_node]


def part_1(text):
    grid = tuple(tuple(map(int, line)) for line in text.strip().split("\n"))
    result = matrix_dijkstra(
        get_neighbours, grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1)
    )
    return result[0]


def get_neighbours_2(node):
    row, col, direction, count = node
    other_directions = {(0, 1), (0, -1), (1, 0), (-1, 0)} - {
        direction,
        (-direction[0], -direction[1]),
    }

    if count < 10:
        yield (row + direction[0], col + direction[1], direction, count + 1)
    if count == 0 or count >= 4:
        for other_direction in other_directions:
            yield (
                row + other_direction[0],
                col + other_direction[1],
                other_direction,
                1,
            )


def matrix_dijkstra_2(grid, start_position, end):
    start = (*start_position, (0, 1), 0)
    min_dist = {start: 0}
    path = {start: [start]}

    not_visited = []
    heapq.heappush(not_visited, (0, start, []))

    while not_visited:
        current = heapq.heappop(not_visited)[1]
        if (current[0], current[1]) == end and current[-1] >= 4:
            end_node = current
            break

        for neighbour in get_neighbours_2(current):
            row, col, _, _ = neighbour
            if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
                continue

            distance = grid[row][col]
            if min_dist.get(neighbour, inf) > distance + min_dist[current]:
                min_dist[neighbour] = distance + min_dist[current]
                path[neighbour] = path[current] + [current]
                heapq.heappush(
                    not_visited, (min_dist[neighbour], neighbour, path[neighbour])
                )

    return min_dist[end_node], path[end_node] + [end_node]


def part_2(text):
    grid = tuple(tuple(map(int, line)) for line in text.strip().split("\n"))
    result = matrix_dijkstra_2(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1))
    return result[0]
