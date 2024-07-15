import re
from math import ceil
from operator import attrgetter

import numpy as np

from pycli.src.grid import Grid, Particle2D, Vector2D

pattern = re.compile(r"-?\d+")

MAX_HEIGHT = 10


def part_1(text, example: bool = False):
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
    print(t_min, t_max)
    for t in range(t_min, t_max + 1):
        assert abs(p_min.get_position(t_min).y - p_max.get_position(t).y) < MAX_HEIGHT

    assert (
        abs(p_min.get_position(t_max + 1).y - p_max.get_position(t_max + 1).y)
        >= MAX_HEIGHT
    )

    # candidates = set(range(100_000))
    # for particle in particles:
    #     py = particle.position.y
    #     vy = particle.speed.y
    #     if vy == 0:
    #         continue
    #     b1, b2 = -py // vy, (MAX_HEIGHT - py) // vy
    #     candidates &= set(range(min(b1, b2), max(b1, b2) + 1))
    #     if len(candidates) == 1:
    #         t = candidates.pop()
    #         break

    #     print(b1, b2)
    #     print(candidates)
    # else:
    #     raise RuntimeError("no candidate")

    for t in range(t_min, t_max + 1):
        positions = [particle.get_position(t) for particle in particles]

        min_x = min(position.x for position in positions)
        min_y = min(position.y for position in positions)
        grid = Grid(
            np.array(
                [
                    [
                        False
                        for _ in range(
                            min_y,
                            max(position.y for position in positions) + 1,
                        )
                    ]
                    for _ in range(
                        min_x,
                        max(position.x for position in positions) + 1,
                    )
                ]
            )
        )
        for position in positions:
            grid[position - Vector2D(min_x, min_y)] = True

        grid.transpose().print()
        print()

    result = "CPJRNKCF"
    return result


def part_2(text, example: bool = False):
    result = None
    return result
