import re
from itertools import chain, combinations
from typing import NamedTuple

from pycli.src.dijkstra import a_star

pattern = re.compile(r"\w+(?:\ generator|\-compatible)")


class Item(NamedTuple):
    element: str
    type: str


def other_type(type):
    return "generator" if type == "microchip" else "microchip"


class Node(NamedTuple):
    current_id: int
    floors: tuple[frozenset[Item], ...]

    def is_valid(self):
        for floor in self.floors:
            if len({item.type for item in floor}) < 2:
                continue

            for item in floor:
                if (
                    item.type == "microchip"
                    and Item(item.element, "generator") not in floor
                ):
                    return False
        return True


def get_sym_invariant(node, items, new_id):
    items = list(items)
    if len(items) == 2 and items[0].element == items[1].element:
        return hash((new_id, ("generator", "microchip")))

    if len(items) == 1:
        item = items[0]
        related = Item(item.element, other_type(item.type))
        related_floor = next(
            idx for idx, floor in enumerate(node.floors) if related in floor
        )
        return hash((new_id, (item.type,), (related_floor, (related.type,))))

    for item in items:
        related = Item(item.element, other_type(item.type))
        related_floor = next(
            idx for idx, floor in enumerate(node.floors) if related in floor
        )


def get_neighbours(node):
    # this function could be improved by removing symmetrical states
    floor = node.floors[node.current_id]
    for direction in (1, -1):
        new_id = node.current_id + direction
        if not 0 <= new_id <= 3:
            continue
        iterator = (
            chain(combinations(floor, 2), combinations(floor, 1))
            if direction == 1
            else combinations(floor, 1)
        )
        for items in map(frozenset, iterator):
            new_floors = list(_floor.copy() for _floor in node.floors)
            new_floors[new_id] |= items
            new_floors[node.current_id] -= items
            neighbour = Node(new_id, tuple(new_floors))
            if neighbour.is_valid():
                yield (neighbour, 1)


def heuristic(node):
    min_floor = min(idx for idx in range(4) if node.floors[idx])
    cost = node.current_id - min_floor
    node_count = 0
    for idx in range(min_floor, 3):
        node_count += len(node.floors[idx])
        if idx == min_floor and node.current_id > min_floor:
            node_count += 1
        if node_count == 1:
            cost += 1
        else:
            cost += 2 * node_count - 3

    return cost


def init(lines):
    floors = []
    for line in lines:
        floor = set()
        for match_ in pattern.findall(line):
            floor.add(Item(*match_.replace("-compatible", " microchip").split()))
        floors.append(frozenset(floor))
    return Node(0, tuple(floors))


def solution(lines):
    start = init(lines)
    end = Node(
        3,
        (
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(chain.from_iterable(start.floors)),
        ),
    )
    result = a_star(start, end, get_neighbours, heuristic=heuristic)[0]
    return result


def part_1(text, example: bool = False):
    return solution(text.strip().split("\n"))


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    additional_elems = (
        "a elerium generator, a elerium-compatible microchip"
        ", a dilithium generator, and a dilithium-compatible microchip."
    )
    lines[0] += additional_elems
    return solution(lines)
