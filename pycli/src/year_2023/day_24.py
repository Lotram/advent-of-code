import math
from fractions import Fraction
from itertools import combinations
from operator import attrgetter
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int
    z: int


class Speed(Point):
    pass


LOWER = 7
UPPER = 27
# LOWER = 200000000000000
# UPPER = 400000000000000


class Line(NamedTuple):
    start: Point
    speed: Speed

    def intersect(self, other):
        xA, yA, _ = self.start
        xB, yB, _ = other.start
        a, b, _ = self.speed
        alpha, beta, _ = other.speed
        if alpha * b - beta * a == 0:
            if a == 0 or b == 0:
                raise ValueError(f"unhandled case {self} {other}")
            return ((xB - xA) / a == (yB - yA) / b > 0) and (
                (xA - xB) / alpha == (yA - yA) / beta > 0
            )

        t = Fraction((alpha * (yA - yB) - beta * (xA - xB)), (a * beta - b * alpha))
        u = Fraction((a * (yB - yA) - b * (xB - xA)), (alpha * b - beta * a))

        x = xA + a * t
        y = yA + b * t
        return LOWER <= x <= UPPER and LOWER <= y <= UPPER and t >= 0 and u >= 0

    @classmethod
    def parse(cls, raw):
        point, speed = raw.split("@")
        return cls(tuple(map(int, point.split(","))), tuple(map(int, speed.split(","))))


def part_1(text, example: bool = False):
    lines = [Line.parse(line) for line in text.strip().split("\n")]
    return sum(1 for line, other in combinations(lines, 2) if line.intersect(other))


mathematica_query = """    Solve[
    Subscript[x, p] + Subscript[a, p] * Subscript[t, i] == 257520024329236 + 21 * Subscript[t, i]  &&
    Subscript[x, p] + Subscript[a, p] * Subscript[t, j] == 227164924449606 + 70 * Subscript[t, j]  &&
    Subscript[x, p] + Subscript[a, p] * Subscript[t, k] == 269125649340143 + 35 * Subscript[t, k] &&
    Subscript[y, p] + Subscript[b, p] * Subscript[t, i] == 69140711609471 + 351 * Subscript[t, i]  &&
    Subscript[y, p] + Subscript[b, p] * Subscript[t, j] == 333280170830371 - 28 * Subscript[t, j]  &&
    Subscript[y, p] + Subscript[b, p] * Subscript[t, k] == 131766988959682 - 337 * Subscript[t, k] &&
    Subscript[z, p] + Subscript[c, p] * Subscript[t, i] == 263886787577054  + 72 * Subscript[t, i]  &&
    Subscript[z, p] + Subscript[c, p] * Subscript[t, j] == 330954002548352  -35 * Subscript[t, j]  &&
    Subscript[z, p] + Subscript[c, p] * Subscript[t, k] == 261281801543906 -  281 * Subscript[t, k],
    {Subscript[x, p], Subscript[y, p], Subscript[z, p], Subscript[a, p], Subscript[b, p], Subscript[c, p], Subscript[t, i], , Subscript[t, j], Subscript[t, k]}
    ]"""


# TODO: Try https://docs.sympy.org/latest/guides/solving/solve-system-of-equations-algebraically.html
def part_2(text, example: bool = False):
    lines = [Line.parse(line) for line in text.strip().split("\n")]
    (x, y, z) = zip(*map(attrgetter("start"), lines))
    (a, b, c) = zip(*map(attrgetter("speed"), lines))
    t = [5, 3, 4, 6, 1]

    # solved with mathematica
    start, speed = (270890255948806, 91424430975421, 238037673112552), (6, 326, 101)
    result = sum(start)
    return result
