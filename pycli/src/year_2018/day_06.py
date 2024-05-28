import heapq
from collections import Counter
from itertools import chain, product

from pycli.src.grid import Vector2D as Vector

inf = float("inf")


def part_1(text, example: bool = False):
    vectors = [Vector(*map(int, line.split(","))) for line in text.strip().split("\n")]
    min_x = min(vec.x for vec in vectors)
    max_x = max(vec.x for vec in vectors)
    min_y = min(vec.y for vec in vectors)
    max_y = max(vec.y for vec in vectors)
    closest = {}
    for x, y in product(range(min_x, max_x + 1), range(min_y, max_y + 1)):
        vector = Vector(x, y)
        ((d1, v1), (d2, _)) = heapq.nsmallest(
            2, (((vector - vec).norm(), vec) for vec in vectors)
        )
        closest[vector] = v1 if d1 < d2 else None

    borders = chain(
        (Vector(x, min_y) for x in range(min_x, max_x)),
        (Vector(x, max_y) for x in range(min_x, max_x)),
        (Vector(min_x, y) for y in range(min_y, max_y)),
        (Vector(max_x, y) for y in range(min_y, max_y)),
    )
    on_border = {closest[border] for border in borders}
    counter = Counter(val for val in closest.values() if val and val not in on_border)
    result = counter.most_common(1)[0][1]
    return result


def part_2(text, example: bool = False):
    max_distance = 32 if example else 10_000
    vectors = [Vector(*map(int, line.split(","))) for line in text.strip().split("\n")]
    min_x = min(vec.x for vec in vectors)
    max_x = max(vec.x for vec in vectors)
    min_y = min(vec.y for vec in vectors)
    max_y = max(vec.y for vec in vectors)
    result = 0
    for x, y in product(range(min_x, max_x + 1), range(min_y, max_y + 1)):
        vector = Vector(x, y)
        if sum((vector - vec).norm() for vec in vectors) < max_distance:
            result += 1

    return result
