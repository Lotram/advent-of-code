import re
from collections import defaultdict
from heapq import nsmallest
from operator import attrgetter
from typing import NamedTuple

import numpy as np
from sympy import Eq, solve
from sympy.abc import x, y, z


class Bot(NamedTuple):
    position: np.ndarray
    r: int

    def reachable(self, other_pos: np.ndarray):
        return np.linalg.norm(other_pos - self.position, 1) <= self.r

    def overlap(self, other):
        return (
            self.r
            + other.r
            - sum(abs(self.position[i] - other.position[i]) for i in range(3))
        )


def parse(text):
    pattern = re.compile(r"-?\d+")
    bots = []
    for line in text.strip().splitlines():
        x, y, z, r = map(int, pattern.findall(line))
        bots.append(Bot(np.array([x, y, z]), r))
    return bots


def part_1(text, example: bool = False):
    bots = parse(text)
    bot = max(bots, key=attrgetter("r"))
    result = sum(bot.reachable(other.position) for other in bots)
    return result


def sign(value):
    return 1 if value >= 0 else -1


def signs(vec):
    return np.array([sign(val) for val in vec])


def part_2(text, example: bool = False):
    # after multiple iterations

    bots = parse(text)
    bot_count = len(bots)
    overlaps = defaultdict(set)
    for i in range(bot_count):
        overlaps[i].add(i)
        for j in range(i + 1, bot_count):
            if bots[i].overlap(bots[j]) >= 0:
                overlaps[i].add(j)
                overlaps[j].add(i)

    while True:
        bot_id, related = nsmallest(1, overlaps.items(), key=lambda item: len(item[1]))[
            0
        ]
        if len(related) < 900:
            overlaps.pop(bot_id)
            for value in overlaps.values():
                value -= {bot_id}
        else:
            break

    bots = [bot for idx, bot in enumerate(bots) if idx in overlaps]
    bot_count = len(bots)
    distances = []

    for i in range(bot_count):
        for j in range(i + 1, bot_count):
            distances.append((bots[i].overlap(bots[j]), (i, j)))

    equations = []
    variables = np.array([x, y, z])
    for dist, (i1, i2) in distances:
        if dist > 0:
            continue
        v1, r1 = bots[i1]
        v2, r2 = bots[i2]
        _signs = signs(v1 - v2)
        equations.append(Eq(sum(_signs * (v1 - variables)), r1))
        equations.append(Eq(sum(_signs * (v2 - variables)), -r2))

    # Problem here if values are < 0
    result = solve(equations, x, y, z, x + y + z)[x + y + z]
    return result
