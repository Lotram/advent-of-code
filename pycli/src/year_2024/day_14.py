import math
import re
from collections import Counter
from itertools import product
from operator import gt, lt
from time import sleep
from typing import NamedTuple

import numpy as np
import rich
from pycli.src.grid import Grid, Vector2D
from rich.align import Align
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel


class Robot(NamedTuple):
    position: Vector2D
    speed: Vector2D

    def get_position(self, t, height, width) -> Vector2D:
        x, y = self.position + t * self.speed

        return Vector2D(x % width, y % height)


pattern = re.compile(r"-?\d+")


def parse(text):
    robots = []
    for line in text.strip().splitlines():
        x, y, vx, vy = map(int, pattern.findall(line))
        robots.append(Robot(Vector2D(x, y), Vector2D(vx, vy)))
    return robots


def build_grid(width, height, positions):
    grid = Grid(np.full((height, width), ".", dtype=str))
    for (x, y), count in positions.items():
        grid[y, x] = str(count)

    return grid


def part_1(text, example: bool = False):
    if example:
        width = 11
        height = 7
    else:
        width = 101
        height = 103

    robots = parse(text)
    positions = Counter(robot.get_position(100, height, width) for robot in robots)

    result = math.prod(
        sum(
            count
            for position, count in positions.items()
            if op_1(position.x, width // 2) and op_2(position.y, height // 2)
        )
        for op_1, op_2 in product([lt, gt], repeat=2)
    )

    # for robot
    return result


def get_renderables(grid, step):
    return Columns([grid, Align(Panel(str(step)), align="center", vertical="middle")])


def part_2(text, example: bool = False):
    if example:
        width = 11
        height = 7
    else:
        width = 101
        height = 103

    robots = parse(text)
    t = 0
    while True:
        t += 1
        positions = Counter(robot.get_position(t, height, width) for robot in robots)
        if max(positions.values()) == 1:
            break

    return t


def print_part_2(text, example: bool = False):
    if example:
        width = 11
        height = 7
    else:
        width = 101
        height = 103

    robots = parse(text)
    t = 7600
    grid = build_grid(
        width, height, Counter(robot.get_position(t, height, width) for robot in robots)
    )
    with Live(get_renderables(grid, t), refresh_per_second=10) as live:
        while True:
            t += 1

            positions = Counter(
                robot.get_position(t, height, width) for robot in robots
            )
            grid = build_grid(width, height, positions)

            live.update(get_renderables(grid, t))
            sleep(0.1)

            if t >= 7640:
                break

        return t
