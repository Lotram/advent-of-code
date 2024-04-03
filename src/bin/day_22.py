from .grid import Vector2D as Vector

# (x, y) coordinates
DIRECTIONS = [
    NORTH := Vector(0, 1),
    EAST := Vector(1, 0),
    SOUTH := Vector(0, -1),
    WEST := Vector(-1, 0),
]


def parse_input(text):
    lines = text.strip().split("\n")
    row_size = len(lines)
    col_size = len(lines[0])
    return {
        Vector(x, -y)
        for y, line in enumerate(lines, -(row_size // 2))
        for x, char in enumerate(line, -(col_size // 2))
        if char == "#"
    }


def next_direction(direction, infected):
    return DIRECTIONS[
        (DIRECTIONS.index(direction) + (1 if infected else -1)) % len(DIRECTIONS)
    ]


def part_1(text):
    infected = parse_input(text)
    current = Vector(0, 0)
    direction = NORTH
    result = 0
    for idx in range(10_000):
        was_infected = current in infected
        direction = next_direction(direction, was_infected)
        infected ^= {current}
        result += not was_infected
        current += direction

    return result


def part_2(text):
    result = None
    return result
