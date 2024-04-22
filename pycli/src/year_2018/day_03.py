import re
from collections import Counter, defaultdict
from itertools import product

from pycli.src.grid import Vector2D


def part_1(text, example: bool = False):
    pattern = re.compile(r"\d+")
    points = [
        Vector2D(int(x), int(y)) + Vector2D(i, j)
        for idx, x, y, w, h in map(pattern.findall, text.strip().split("\n"))
        for i, j in product(range(int(w)), range(int(h)))
    ]
    counter = Counter(points)
    result = sum(1 for val in counter.values() if val > 1)
    return result


def part_2(text, example: bool = False):
    pattern = re.compile(r"\d+")
    lines = text.strip().split("\n")
    points = defaultdict(list)
    for idx, x, y, w, h in map(pattern.findall, lines):
        for i, j in product(range(int(w)), range(int(h))):
            points[Vector2D(int(x), int(y)) + Vector2D(i, j)].append(idx)

    candidates = set(map(str, range(1, len(lines) + 1)))
    for indexes in points.values():
        if len(indexes) > 1:
            candidates -= set(indexes)

    assert len(candidates) == 1
    result = candidates.pop()
    return result
