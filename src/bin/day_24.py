from fractions import Fraction
from itertools import combinations
from typing import NamedTuple

from sympy import Symbol
from sympy.solvers import solve


class Point(NamedTuple):
    x: int
    y: int
    z: int


class Speed(Point):
    pass


# LOWER = 7
# UPPER = 27
LOWER = 200000000000000
UPPER = 400000000000000


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


def part_1(text):
    lines = [Line.parse(line) for line in text.strip().split("\n")]
    return sum(1 for line, other in combinations(lines, 2) if line.intersect(other))


def part_2(text):

    lines = [Line.parse(line) for line in text.strip().split("\n")]
    axes = [Symbol(s) for s in ["x", "y", "z"]]
    speeds = [Symbol(s) for s in ["a", "b", "c"]]
    durations = [Symbol(s) for s in ["t", "u", "v"]]

    equations = [
        axis
        - line.start[axis_idx]
        + (speed - line.speed[axis_idx]) * durations[line_idx]
        for line_idx, line in enumerate(lines[:3])
        for axis_idx, (axis, speed) in enumerate(zip(axes, speeds))
    ]

    solution = solve(equations)[0]
    result = sum(solution[axis] for axis in axes)
    return result
