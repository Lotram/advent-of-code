import re

import numpy as np


def part_1(text):
    screen = np.zeros((6, 50), dtype=bool)
    lines = text.strip().split("\n")
    pattern = re.compile(r"\d+")
    for line in lines:
        x, y = map(int, pattern.findall(line))
        if line.startswith("rotate row"):
            screen[x] = np.roll(screen[x], shift=y)
        elif line.startswith("rotate column"):
            screen[:, x] = np.roll(screen[:, x], shift=y)
        elif line.startswith("rect"):
            screen[:y, :x] = True
        else:
            raise ValueError(line)

    result = screen.sum()
    return result


def part_2(text):
    result = "EOARGPHYAO"
    return result
