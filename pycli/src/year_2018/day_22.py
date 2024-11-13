import re
import types
from functools import cache
from typing import NamedTuple

from pycli.src.dijkstra import dijkstra


consts = types.SimpleNamespace()


@cache
def geologic_index(x, y):
    match (x, y):
        case (0, 0):
            return 0
        case (consts.X, consts.Y):
            return 0
        case (_x, 0):
            return _x * 16807
        case (0, _y):
            return _y * 48271
        case _:
            return erosion_level(x - 1, y) * erosion_level(x, y - 1)


@cache
def erosion_level(x, y):
    return (geologic_index(x, y) + consts.DEPTH) % 20183


def part_1(text, example: bool = False):
    consts.DEPTH, consts.X, consts.Y = map(int, re.findall(r"\d+", text))
    result = sum(
        erosion_level(x, y) % 3
        for x in range(consts.X + 1)
        for y in range(consts.Y + 1)
    )
    return result


NEITHER = 0
TORCH = 1
CLIMBING = 2


class State(NamedTuple):
    x: int
    y: int
    gear: int


ALLOWED_GEARS = [{TORCH, CLIMBING}, {NEITHER, CLIMBING}, {TORCH, NEITHER}]

OTHER_GEAR = {
    (type_, equipped): (ALLOWED_GEARS[type_] - {equipped}).pop()
    for type_ in range(3)
    for equipped in range(3)
    if equipped in ALLOWED_GEARS[type_]
}


def get_neighbours(state):
    x, y, gear = state
    current_type = erosion_level(x, y) % 3
    other_gear = OTHER_GEAR[current_type, gear]
    yield (State(x, y, other_gear), 7)
    for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        if (_x := dx + x) < 0 or (_y := dy + y) < 0:
            continue
        next_type = erosion_level(_x, _y) % 3
        if gear in ALLOWED_GEARS[next_type]:
            yield (State(_x, _y, gear), 1)


def part_2(text, example: bool = False):
    consts.DEPTH, consts.X, consts.Y = map(int, re.findall(r"\d+", text))
    start = State(0, 0, TORCH)
    end = State(consts.X, consts.Y, TORCH)
    stop_condition = end.__eq__
    result = dijkstra(start, stop_condition, get_neighbours)[0]
    return result
