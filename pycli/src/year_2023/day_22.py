import heapq
from collections import defaultdict
from operator import attrgetter, methodcaller
from typing import NamedTuple

from pydantic import BaseModel


class Point(BaseModel):
    x: int
    y: int
    z: int

    @classmethod
    def from_tuple(cls, tuple):
        return cls(x=tuple[0], y=tuple[1], z=tuple[2])


class Brick(BaseModel):
    start: Point
    end: Point

    @classmethod
    def parse(cls, line):
        start, end = map(methodcaller("split", ","), line.split("~"))
        return cls(start=Point.from_tuple(start), end=Point.from_tuple(end))

    def lower(self, z):
        height = self.end.z - self.start.z + 1
        self.start.z = z
        self.end.z = z + height - 1


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    bricks = sorted(
        (Brick.parse(line) for line in lines), key=attrgetter("start.z", "end.z")
    )
    supports = defaultdict(set)
    supported_by = defaultdict(set)
    highest_positions = {}
    for id, brick in enumerate(bricks):
        new_start_z = (
            max(
                highest_positions.get((x, y), (0, None))[0]
                for x in range(brick.start.x, brick.end.x + 1)
                for y in range(brick.start.y, brick.end.y + 1)
            )
            + 1
        )
        brick.lower(new_start_z)
        new_end_z = brick.end.z

        for x in range(brick.start.x, brick.end.x + 1):
            for y in range(brick.start.y, brick.end.y + 1):
                if (x, y) in highest_positions:
                    old_z, old_id = highest_positions[x, y]
                    if old_z == new_start_z - 1:
                        supported_by[id].add(old_id)
                        supports[old_id].add(id)

                highest_positions[x, y] = (new_end_z, id)

    candidates = set()

    for idx in range(len(bricks)):
        if all(
            bool(supported_by[supported] - {idx})
            for supported in supports.get(idx, set())
        ):
            candidates.add(idx)

    result = len(candidates)
    return result


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    bricks = sorted(
        (Brick.parse(line) for line in lines), key=attrgetter("start.z", "end.z")
    )
    supports = defaultdict(set)
    supported_by = defaultdict(set)
    highest_positions = {}
    for id, brick in enumerate(bricks):
        new_start_z = (
            max(
                highest_positions.get((x, y), (0, None))[0]
                for x in range(brick.start.x, brick.end.x + 1)
                for y in range(brick.start.y, brick.end.y + 1)
            )
            + 1
        )
        brick.lower(new_start_z)
        new_end_z = brick.end.z

        for x in range(brick.start.x, brick.end.x + 1):
            for y in range(brick.start.y, brick.end.y + 1):
                if (x, y) in highest_positions:
                    old_z, old_id = highest_positions[x, y]
                    if old_z == new_start_z - 1:
                        supported_by[id].add(old_id)
                        supports[old_id].add(id)

                highest_positions[x, y] = (new_end_z, id)

    def delete_node(brick_start):
        queue = []

        def key(brick):
            return bricks[brick].start.z

        heapq.heappush(queue, (key(brick_start), brick_start))
        deleted = set()
        while queue:
            current = heapq.heappop(queue)[1]
            if current == brick_start or supported_by[current] <= deleted:
                deleted.add(current)
                for child in supports[current]:
                    heapq.heappush(queue, (key(child), child))

        return len(deleted) - 1

    result = 0
    for idx in list(supports):
        result += delete_node(idx)
    return result
