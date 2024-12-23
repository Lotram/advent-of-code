from collections import deque

from .intcode import ListIntCodeComputer


j = 1j
directions = {"^": j, "v": -j, ">": 1, "<": -1}


def build_scaffolds(characters):
    row = 0
    col = 0
    scaffolds = set()
    for char in characters:
        if char == "\n":
            row += 1
            col = 0
            continue

        if char in {"^", "<", "v", ">"}:
            start = (col - row * j, directions[char])

        if char != ".":
            scaffolds.add(col - row * j)
        col += 1

    return (start, scaffolds)


def part_1(text, example: bool = False):
    computer = ListIntCodeComputer.from_text(text)
    computer.run()

    _, scaffolds = build_scaffolds(map(chr, computer.get_all()))
    intersections = {
        scaffold
        for scaffold in scaffolds
        if all((scaffold + direction) in scaffolds for direction in directions.values())
    }
    result = int(sum(-scaffold.imag * scaffold.real for scaffold in intersections))

    return result


def build_path(start, scaffolds):
    position, direction = start
    moves = []
    move = 0
    visited = set()
    while True:
        visited.add(position)
        if position + direction in scaffolds:
            move += 1
            position += direction
            continue

        try:
            next_turn = next(
                turn for turn in {j, -j} if turn * direction + position in scaffolds
            )
        except StopIteration:
            if move:
                moves.append(str(move))
            break

        direction *= next_turn
        if move:
            moves.append(str(move))

        moves.append("L" if next_turn == j else "R")
        move = 0

    assert visited == scaffolds
    return moves


def to_ascii(routine):
    return [ord(char) for char in routine.rstrip(",")] + [ord("\n")]


possible_patterns = "ABCDEFGH"


def find_patterns(path, patterns, next_pattern="A"):
    if sum(count for count, _ in patterns.values()) > 10 or any(
        len(to_ascii(pattern)) > 21 for _, pattern in patterns.values()
    ):
        return False
    if not (set(path) - set(possible_patterns)):
        return (path, patterns)

    for size in range(5, 22):
        sub = path.lstrip(possible_patterns)[:size]
        if set(sub) & set(possible_patterns):
            break
        if sub not in path.lstrip(possible_patterns)[size:]:
            continue

        count = path.count(sub)
        if value := find_patterns(
            path.replace(sub, next_pattern),
            {**patterns, next_pattern: (count, sub)},
            chr(ord(next_pattern) + 1),
        ):
            return value


def build_inputs(routine, patterns):
    inputs = to_ascii(",".join(list(routine)))
    for _, pattern in patterns.values():
        inputs.extend(to_ascii(pattern))

    inputs.extend(to_ascii("n"))
    return inputs


def part_2(text, example: bool = False):
    computer = ListIntCodeComputer.from_text(text)
    computer.run()
    start, scaffolds = build_scaffolds(map(chr, computer.get_all()))
    path = build_path(start, scaffolds)
    routine, patterns = find_patterns(",".join(path) + ",", {})

    computer.reset()
    computer.memory[0] = 2
    computer.io_handler.inputs = deque(build_inputs(routine, patterns))
    computer.run()
    result = computer.get_all()[-1]
    return result
