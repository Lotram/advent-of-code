moves = {"^": (1, 0), "v": (-1, 0), "<": (0, -1), ">": (0, 1)}


def add(position, move):
    return (position[0] + move[0], position[1] + move[1])


def part_1(text, example: bool = False):
    line = text.split("\n")[0]
    current = (0, 0)
    positions = {current}
    for char in line:
        current = add(current, moves[char])
        positions.add(current)
    return len(positions)


def part_2(text, example: bool = False):
    line = text.split("\n")[0]
    santa = robot = (0, 0)
    positions = {santa}
    for idx, char in enumerate(line):
        if idx % 2 == 0:
            santa = add(santa, moves[char])
            positions.add(santa)
        else:
            robot = add(robot, moves[char])
            positions.add(robot)

    return len(positions)
