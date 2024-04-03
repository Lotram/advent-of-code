from .grid import Point, Vector


def part_1(text, example: bool = False):
    current_position = Point(0, 0)
    current_direction = Vector(1, 0)
    for direction, *count in text.strip().split(", "):
        blocks = int("".join(count))
        if direction == "L":
            current_direction = Vector(-current_direction[1], current_direction[0])
        else:
            current_direction = Vector(current_direction[1], -current_direction[0])

        current_position += blocks * current_direction

    return abs(current_position.row) + abs(current_position.col)


def part_2(text, example: bool = False):
    current_position = Point(0, 0)
    current_direction = Vector(1, 0)
    visited = {current_position}
    for direction, *count in text.strip().split(", "):
        blocks = int("".join(count))
        if direction == "L":
            current_direction = Vector(-current_direction[1], current_direction[0])
        else:
            current_direction = Vector(current_direction[1], -current_direction[0])

        for _count in range(1, blocks + 1):
            block = current_position + _count * current_direction
            if block in visited:
                return abs(block.row) + abs(block.col)
            visited.add(block)

        current_position += blocks * current_direction
    raise ValueError("a intersection should have been found")
