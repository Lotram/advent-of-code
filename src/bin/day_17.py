import heapq
from hashlib import md5
from typing import NamedTuple

from .dijkstra import a_star
from .grid import Point

inf = float("inf")


DIRECTIONS = {"U": Point(-1, 0), "D": Point(1, 0), "L": Point(0, -1), "R": Point(0, 1)}


class Node(NamedTuple):
    position: Point
    data: str
    open_doors: tuple[bool, bool, bool, bool]


def stop_condition(node):
    return node.position == Point(3, 3)


def heuristic(node):
    return 6 - node.position.row - node.position.col


def get_open_doors(data) -> tuple[bool, bool, bool, bool]:
    return tuple(char in "bcdef" for char in md5(data.encode()).hexdigest()[:4])


def get_neighbours(node):
    for idx, (dir_name, direction) in enumerate(DIRECTIONS.items()):
        new_position = node.position + direction
        if (
            node.open_doors[idx]
            and 0 <= new_position.row < 4
            and 0 <= new_position.col < 4
        ):
            data = node.data + dir_name
            yield (Node(new_position, node.data + dir_name, get_open_doors(data)), 1)


def part_1(text):
    data = text.strip()
    start = Node(Point(0, 0), data, get_open_doors(data))
    cost, path = a_star(start, stop_condition, get_neighbours, heuristic)
    result = path[-1].data.removeprefix(data)

    return result


def modified_dijkstra(start, stop_condition, get_neighbours):
    min_dist = {start: 0}
    not_visited = []
    heapq.heappush(not_visited, (0, start))
    max_value = -inf
    while not_visited:
        current = heapq.heappop(not_visited)[1]
        if stop_condition(current):
            max_value = max(max_value, min_dist[current])
            continue

        for neighbour, distance in get_neighbours(current):
            if min_dist.get(neighbour, -inf) < distance + min_dist[current]:
                min_dist[neighbour] = distance + min_dist[current]
                heapq.heappush(not_visited, (min_dist[neighbour], neighbour))

    return max_value


def part_2(text):
    data = text.strip()
    start = Node(Point(0, 0), data, get_open_doors(data))
    cost = modified_dijkstra(start, stop_condition, get_neighbours)

    return cost
