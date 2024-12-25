import math
import re
from collections import Counter
from itertools import product
from operator import gt, lt

import numpy as np
from pycli.src.grid import Grid


pattern = re.compile(r"-?\d+")


def parse(text):
    robots = []
    for line in text.strip().splitlines():
        x, y, vx, vy = map(int, pattern.findall(line))
        robots.append((complex(x, y), complex(vx, vy)))
    return robots


def part_1(text, example: bool = False):
    if example:
        width = 11
        height = 7
    else:
        width = 101
        height = 103

    def get_position(position, speed, t):
        position = position + speed * t
        return (int(position.real % width), int(position.imag % height))

    robots = parse(text)
    positions = Counter(
        get_position(position, speed, 100) for (position, speed) in robots
    )

    result = math.prod(
        sum(
            count
            for position, count in positions.items()
            if op_1(position[0], width // 2) and op_2(position[1], height // 2)
        )
        for op_1, op_2 in product([lt, gt], repeat=2)
    )

    # for robot
    return result


def build_grid(width, height, positions):
    grid = Grid(np.full((height, width), ".", dtype=str))

    for val in positions:
        grid[int(val.imag)][int(val.real)] = "#"
    return grid


PRINT = False


def solve(robots, height, width):
    t = 0

    while True:
        t += 1
        positions = set()
        for robot in robots:
            position = complex(
                int((robot[0] + t * robot[1]).real) % width,
                int((robot[0] + t * robot[1]).imag) % height,
            )
            if position in positions:
                break

            positions.add(position)

        else:
            break
    if PRINT:
        build_grid(width, height, positions).print()
    return t


def part_2(text, example: bool = False):
    if example:
        width = 11
        height = 7
    else:
        width = 101
        height = 103

    robots = parse(text)
    return solve(robots, height, width)
