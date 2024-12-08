from collections import defaultdict
from itertools import combinations
from math import gcd
from operator import add, sub


j = 1j


def in_map(value, row_count, col_count):
    return 0 <= value.real < col_count and 0 <= value.imag < row_count


def parse(text):
    lines = text.strip().splitlines()
    antennas = defaultdict(list)
    col_count = len(lines[0])
    row_count = len(lines)
    for row_idx, line in enumerate(text.strip().splitlines()):
        for col_idx, char in enumerate(line):
            if char != ".":
                antennas[char].append(col_idx + (row_count - row_idx - 1) * j)

    return antennas, row_count, col_count


def part_1(text, example: bool = False):
    antennas, row_count, col_count = parse(text)
    antinodes = set()
    for _antennas in antennas.values():
        for antenna_1, antenna_2 in combinations(_antennas, r=2):
            diff = antenna_1 - antenna_2
            for antinode in [antenna_1 + diff, antenna_2 - diff]:
                if 0 <= antinode.real < col_count and 0 <= antinode.imag < row_count:
                    antinodes.add(antinode)

    return len(antinodes)


def part_2(text, example: bool = False):
    antennas, row_count, col_count = parse(text)
    antinodes = set()
    for _antennas in antennas.values():
        for antenna_1, antenna_2 in combinations(_antennas, r=2):
            diff = antenna_1 - antenna_2
            diff /= gcd(int(diff.real), int(diff.imag))
            antinode = antenna_1
            for op in [add, sub]:
                antinode = antenna_1
                while 0 <= antinode.real < col_count and 0 <= antinode.imag < row_count:
                    antinodes.add(antinode)
                    antinode = op(antinode, diff)

    return len(antinodes)
