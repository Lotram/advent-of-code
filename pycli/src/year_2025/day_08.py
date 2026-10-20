import heapq
import math
from itertools import combinations

from pycli.src.grid import Vector3D
from pycli.src.karger_min_cut import DisjointSet


def part_1(text, example: bool = False):
    size = 10 if example else 1000

    positions = [Vector3D(*map(int, line.split(","))) for line in text.splitlines()]

    edges = heapq.nsmallest(
        size, (((p2 - p1).norm(2), p1, p2) for p1, p2 in combinations(positions, 2))
    )
    nodes = {position for edge in edges for position in edge[1:3]}

    ds = DisjointSet.from_sequence(nodes)
    for _, src, dest in edges:
        ds.union(src, dest)

    biggest_sizes = heapq.nlargest(3, (ds.elements[root].size for root in ds.roots))
    result = math.prod(biggest_sizes)
    return result


def part_2(text, example: bool = False):
    positions = [Vector3D(*map(int, line.split(","))) for line in text.splitlines()]

    edges = sorted(
        (((p2 - p1).norm(2), p1, p2) for p1, p2 in combinations(positions, 2)),
        reverse=True,
    )

    ds = DisjointSet.from_sequence(positions)
    while len(ds.roots) > 1:
        _, src, dest = edges.pop()
        ds.union(src, dest)

    result = src.x * dest.x
    return result
