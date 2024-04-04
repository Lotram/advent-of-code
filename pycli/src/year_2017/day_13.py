import re

from sympy.ntheory.modular import symmetric_residue

pattern = re.compile(r"\d+")


def part_1(text, example: bool = False):
    values = [map(int, pattern.findall(line)) for line in text.strip().split("\n")]
    result = sum(
        depth * range
        for depth, range in values
        if symmetric_residue(depth % (2 * (range - 1)), 2 * (range - 1)) == 0
    )
    return result


def part_2(text, example: bool = False):
    values = [
        tuple(map(int, pattern.findall(line))) for line in text.strip().split("\n")
    ]
    result = 0
    while any(
        symmetric_residue((result + depth) % (2 * (range - 1)), 2 * (range - 1)) == 0
        for depth, range in values
    ):
        result += 1
    return result
