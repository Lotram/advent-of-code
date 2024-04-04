from functools import cache

MOVES = dict(D=(1, 0), L=(0, -1), R=(0, 1), U=(-1, 0))


def add(pos, dir):
    return (pos[0] + dir[0], pos[1] + dir[1])


def sign(x, y):
    return (x > y) - (x < y)


@cache
def move_tail(head, _tail):
    tail = list(_tail)
    for idx in (0, 1):
        if abs(head[idx] - tail[idx]) >= 2:
            tail[idx] = int((head[idx] + tail[idx]) / 2)
            tail[1 - idx] += sign(head[1 - idx], tail[1 - idx])
            break

    return tuple(tail)


def solution(moves, size):
    knots = [(0, 0)] * size
    tail_positions = {knots[-1]}
    for direction, count in moves:
        for _ in range(count):
            knots[0] = add(knots[0], direction)
            for idx in range(1, size):
                knots[idx] = move_tail(knots[idx - 1], knots[idx])

            tail_positions.add(knots[-1])
    return len(tail_positions)


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    moves = [(MOVES[line[0]], int(line[2:])) for line in lines]
    return solution(moves, size=2)


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    moves = [(MOVES[line[0]], int(line[2:])) for line in lines]
    return solution(moves, size=10)
