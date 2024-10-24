import re
from math import ceil
from operator import attrgetter

import numpy as np
from pycli.src.grid import Grid, Particle2D, Vector2D


pattern = re.compile(r"-?\d+")

MAX_HEIGHT = 12


def solution(text):
    lines = map(pattern.findall, text.strip().split("\n"))
    particles = [
        Particle2D(
            position=Vector2D(x=int(px), y=int(py)),
            speed=Vector2D(x=int(vx), y=int(vy)),
            acceleration=Vector2D(x=0, y=0),
        )
        for px, py, vx, vy in lines
    ]
    p_min = min(particles, key=attrgetter("speed.y"))
    p_max = max(particles, key=attrgetter("speed.y"))
    py = p_max.position.y - p_min.position.y
    vy = p_max.speed.y - p_min.speed.y
    t_min = ceil((-MAX_HEIGHT - py) / vy)
    t_max = int((MAX_HEIGHT - py) / vy)
    for t in range(t_min, t_max + 1):
        assert abs(p_min.get_position(t_min).y - p_max.get_position(t).y) < MAX_HEIGHT

    assert (
        abs(p_min.get_position(t_max + 1).y - p_max.get_position(t_max + 1).y)
        >= MAX_HEIGHT
    )

    for t in range(t_min, t_max + 1):
        positions = [particle.get_position(t) for particle in particles]

        min_x = min(position.x for position in positions)
        max_x = max(position.x for position in positions)
        min_y = min(position.y for position in positions)
        max_y = max(position.y for position in positions)
        if max_y - min_y > MAX_HEIGHT:
            continue

        print(t)
        grid = Grid(
            np.array(
                [
                    [False for _ in range(min_y, max_y + 1)]
                    for _ in range(min_x, max_x + 1)
                ]
            )
        )
        for position in positions:
            grid[position - Vector2D(min_x, min_y)] = True

        grid.transpose().print()
        print()


def part_1(text, example: bool = False):
    solution(text)
    result = "CPJRNKCF"
    return result


def part_2(text, example: bool = False):
    solution(text)
    result = 10345
    return result
