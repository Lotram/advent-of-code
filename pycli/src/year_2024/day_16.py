import heapq
from collections import defaultdict
from functools import partial
from typing import NamedTuple

from pycli.src.dijkstra import dijkstra
from pycli.src.grid import DIRECTIONS, EAST, Grid, Vector


class State(NamedTuple):
    position: Vector
    direction: Vector


def get_neighbours(maze, state):
    position, direction = state
    yield (State(position, direction.rotate(1)), 1000)
    yield (State(position, direction.rotate(-1)), 1000)

    if (next_position := position + direction) in maze:
        yield (State(next_position, direction), 1)


def parse(text) -> tuple[set[Vector], Vector, Vector]:
    grid = Grid.from_text(text)
    start = grid.find("S")
    end = grid.find("E")
    maze = {position for position, value in grid.flat_iter() if value != "#"}

    return maze, start, end


def stop_condition(end, state):
    return state.position == end


def part_1(text, example: bool = False):
    maze, start, end = parse(text)
    _stop_condition = partial(stop_condition, end)
    _get_neighbours = partial(get_neighbours, maze)
    result, _ = dijkstra(State(start, EAST), _stop_condition, _get_neighbours)
    return result


def dijkstra_all_paths(start, get_neighbours, end_position):
    min_dist = {start: 0}
    prev = defaultdict(list)
    not_visited = []
    heapq.heappush(not_visited, (0, start))
    while not_visited:
        current = heapq.heappop(not_visited)[1]
        for neighbour, distance in get_neighbours(current):
            new_dist = distance + min_dist[current]
            _min_dist = min_dist.get(neighbour, float("inf"))
            if _min_dist > new_dist:
                min_dist[neighbour] = distance + min_dist[current]
                prev[neighbour] = [current]
                weight = min_dist[neighbour]
                heapq.heappush(not_visited, (weight, neighbour))
            elif _min_dist == new_dist:
                prev[neighbour].append(current)

    def possible_nodes(node, nodes):
        nodes.add(node)
        if prev[node] == []:
            return nodes  # Base case: start node

        _nodes = set()
        for predecessor in prev[node]:
            _nodes.add(predecessor)
            _nodes |= possible_nodes(predecessor, nodes)
        return nodes | _nodes

    possible_ends = [State(end_position, DIRECTION) for DIRECTION in DIRECTIONS]
    min_distance = min(min_dist[end] for end in possible_ends)
    ends = [end for end in possible_ends if min_dist[end] == min_distance]
    return len({node.position for end in ends for node in possible_nodes(end, set())})


def part_2(text, example: bool = False):
    maze, start, end = parse(text)
    _get_neighbours = partial(get_neighbours, maze)
    result = dijkstra_all_paths(State(start, EAST), _get_neighbours, end)

    return result
