from collections import defaultdict

from .grid import Vector2D as Vector

# (x, y) coordinates
DIRECTIONS = [
    NORTH := Vector(0, 1),
    EAST := Vector(1, 0),
    SOUTH := Vector(0, -1),
    WEST := Vector(-1, 0),
]


def parse_input(text, infected_value):
    lines = text.strip().split("\n")
    row_size = len(lines)
    col_size = len(lines[0])
    return {
        Vector(x, -y): infected_value
        for y, line in enumerate(lines, -(row_size // 2))
        for x, char in enumerate(line, -(col_size // 2))
        if char == "#"
    }


def next_direction(direction: Vector, count: int):
    turn = -1 if count % 2 == 0 else 1
    return DIRECTIONS[(DIRECTIONS.index(direction) + turn) % len(DIRECTIONS)]


def part_1(text, example: bool = False):
    infection_count = defaultdict(int, parse_input(text, infected_value=1))
    current = Vector(0, 0)
    direction = NORTH
    result = 0
    for idx in range(10_000):
        prev_count = infection_count[current]
        direction = next_direction(direction, prev_count)
        infection_count[current] += 1
        result += prev_count % 2 == 0
        current += direction

    return result


def next_direction_2(direction: Vector, count: int):
    match count % 4:
        case 0:
            turn = -1
        case 1:
            turn = 0
        case 2:
            turn = 1
        case 3:
            turn = 2
    return DIRECTIONS[(DIRECTIONS.index(direction) + turn) % len(DIRECTIONS)]


def part_2(text, example: bool = False):
    infection_count = defaultdict(int, parse_input(text, infected_value=2))
    current = Vector(0, 0)
    direction = NORTH
    result = 0
    for idx in range(10_000_000):
        prev_count = infection_count[current]
        direction = next_direction_2(direction, prev_count)
        infection_count[current] += 1
        result += prev_count % 4 == 1
        current += direction

    return result
