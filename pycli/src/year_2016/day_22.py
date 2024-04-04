import re
from bisect import bisect
from operator import attrgetter, neg
from typing import NamedTuple

import numpy as np

from pycli.src.grid import Grid, Vector

PATTERN = re.compile(r"\d+")


class Disk(NamedTuple):
    used: int
    available: int


class Node(NamedTuple):
    point: Vector
    disk: Disk


def parse(text: str) -> list[Node]:
    disks = []
    for line in text.strip().split("\n")[2:]:
        row, col, total, used, available, used_percent = map(int, PATTERN.findall(line))
        disks.append(Node(Vector(row, col), Disk(used, available)))

    return disks


def part_1(text, example: bool = False):
    disks = [node.disk for node in parse(text)]
    availables = sorted(map(attrgetter("available"), disks), reverse=True)
    result = 0
    for disk in disks:
        if not disk.used:
            continue
        result += bisect(availables, -disk.used, key=neg) - (
            disk.used <= disk.available
        )
    return result


BIG_DISK_THRESHOLD = 100


def get_value(node):
    if node.disk.used >= BIG_DISK_THRESHOLD:
        return "#"
    elif node.disk.used == 0:
        return "_"
    else:
        return "."


def part_2(text, example: bool = False):
    """
    The input as the same shape as the exemple:
    * 1 empty node
    * several nodes too big to move
    * all other nodes can be moved, but can't accept data from two other nodes at the same time

    There is a line of full disks between the empty disk and the target that we need
    to bypass
    """
    nodes = parse(text)
    row_size = nodes[-1].point.row + 1
    values = [get_value(node) for node in nodes]
    grid = Grid(np.array(np.split(np.array(values), row_size)))
    empty = grid.find("_")
    first_full = grid.find("#")

    first_available = Vector(first_full.row - 1, first_full.col)
    result = int(
        (empty - first_available).norm(p=1)
        + (first_available - Vector(row_size - 2, 0)).norm(p=1)
        + 5 * (row_size - 2)
        + 1
    )
    return result
