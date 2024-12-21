from functools import cache
from itertools import pairwise, permutations

from pycli.src.grid import Vector2D as Vec


numeric_keypad = {
    "0": Vec(1, 0),
    "A": Vec(2, 0),
    "1": Vec(0, 1),
    "2": Vec(1, 1),
    "3": Vec(2, 1),
    "4": Vec(0, 2),
    "5": Vec(1, 2),
    "6": Vec(2, 2),
    "7": Vec(0, 3),
    "8": Vec(1, 3),
    "9": Vec(2, 3),
}


# starts on y = -1 to have A at the same position on both keypads
directional_keypad = {
    "<": Vec(0, -1),
    "v": Vec(1, -1),
    ">": Vec(2, -1),
    "^": Vec(1, 0),
    "A": Vec(2, 0),
}

keypads = {**numeric_keypad, **directional_keypad}


@cache
def get_sequences(start, end):
    x, y = keypads[end] - keypads[start]
    sequence = ["<"] * -x + [">"] * x + ["v"] * -y + ["^"] * y

    # all possible sequences to go from start to end
    sequences = set(permutations(sequence))

    # remove all forbidden sequences
    if start in {"0", "A"} and end in {"1", "4", "7"}:
        sequences = {sequence for sequence in sequences if sequence[:-x] != ("<",) * -x}

    if end in {"0", "A"} and start in {"1", "4", "7"}:
        sequences = {sequence for sequence in sequences if sequence[:-y] != ("v",) * -y}

    if start in {"^", "A"} and end == "<":
        sequences = {sequence for sequence in sequences if sequence[:-x] != ("<",) * -x}

    if end in {"^", "A"} and start == "<":
        sequences = {sequence for sequence in sequences if sequence[:y] != ("^",) * y}

    return [_sequence + ("A",) for _sequence in sequences]


@cache
def get_pair_length(pair, depth, max_depth):
    sequences = get_sequences(*pair)
    if depth == max_depth:
        return len(sequences[0])

    sequences = [("A",) + sequence for sequence in sequences]

    return min(
        sum(
            get_pair_length(_pair, depth + 1, max_depth) for _pair in pairwise(sequence)
        )
        for sequence in sequences
    )


def get_code_length(code, robot_count):
    return sum(get_pair_length(pair, 0, robot_count) for pair in pairwise("A" + code))


def solve(text, robot_count):
    return sum(
        get_code_length(code, robot_count) * int(code[:-1])
        for code in text.strip().splitlines()
    )


def part_1(text, example: bool = False):
    result = solve(text, 2)
    return result


def part_2(text, example: bool = False):
    result = solve(text, 25)
    return result
