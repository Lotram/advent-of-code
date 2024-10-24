from pycli.src.grid import Vector


directions = {
    "ne": Vector(1, 1),
    "n": Vector(2, 0),
    "nw": Vector(1, -1),
    "sw": Vector(-1, -1),
    "s": Vector(-2, 0),
    "se": Vector(-1, 1),
}


def distance(position):
    row, col = abs(position.row), abs(position.col)
    return col + max(0, row - col) // 2


def part_1(text, example: bool = False):
    end = sum((directions[_dir] for _dir in text.strip().split(",")), Vector(0, 0))
    result = distance(end)
    return result


def part_2(text, example: bool = False):
    position = Vector(0, 0)
    result = 0
    for direction in text.strip().split(","):
        position += directions[direction]
        result = max(distance(position), result)

    return result
