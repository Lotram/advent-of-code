from collections import deque

import numpy as np

from .day_10 import knot_hash
from .grid import Grid


def build_array(text):
    return [
        [
            char == "1"
            for char in f"{int(knot_hash(f'{text.strip()}-{idx}'), 16):0>128b}"
        ]
        for idx in range(128)
    ]


def part_1(text):
    result = np.sum(build_array(text))
    return result


def part_2(text):
    grid = Grid(build_array(text))
    result = 0
    visited = set()
    remaining = set(grid.find_iter(True))
    while remaining:
        result += 1
        point = remaining.pop()
        queue = deque([point])
        while queue:
            current = queue.popleft()
            visited.add(current)
            for neighbour, value in grid.neighbours(current):
                if value and neighbour not in visited:
                    queue.append(neighbour)

        remaining -= visited

    return result
