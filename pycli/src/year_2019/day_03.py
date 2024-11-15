from pycli.src.grid import Vector2D as Vector


DIRECTIONS = {
    "U": Vector(-1, 0),
    "D": Vector(1, 0),
    "L": Vector(0, -1),
    "R": Vector(0, 1),
}


def part_1(text, example: bool = False):
    wires = []
    for line in text.strip().splitlines():
        positions = set()
        current = Vector(0, 0)
        for move in line.split(","):
            for _ in range(int(move[1:])):
                current += DIRECTIONS[move[0]]
                positions.add(current)

        wires.append(positions)
    result = int(min(position.norm(p=1) for position in wires[0] & wires[1]))
    return result


def part_2(text, example: bool = False):
    wires = []
    wire_delays = []
    for line in text.strip().splitlines():
        positions = set()
        delays = {}
        current = Vector(0, 0)
        steps = 0
        for move in line.split(","):
            for _ in range(int(move[1:])):
                current += DIRECTIONS[move[0]]
                positions.add(current)
                steps += 1
                delays.setdefault(current, steps)

        wires.append(positions)
        wire_delays.append(delays)
    result = min(
        wire_delays[0][position] + wire_delays[1][position]
        for position in wires[0] & wires[1]
    )

    return result
