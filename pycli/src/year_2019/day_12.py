import math
import re
from collections.abc import Callable
from itertools import groupby
from typing import NamedTuple


pattern = re.compile(r"-?\d+")


class Moon(NamedTuple):
    idx: int
    position: list[int]
    speed: list[int]

    def move(self):
        for axis in range(3):
            self.position[axis] += self.speed[axis]

    @property
    def energy(self):
        return sum(map(abs, self.position)) * sum(map(abs, self.speed))


def parse(text: str):
    positions = [
        list(map(int, pattern.findall(line))) for line in text.strip().splitlines()
    ]
    return [
        Moon(idx=idx, position=position, speed=[0, 0, 0])
        for idx, position in enumerate(positions)
    ]


def key(axis: int) -> Callable[[Moon], int]:
    def _key(item: Moon) -> int:
        return item.position[axis]

    return _key


def _apply_gravity(moons, moon_count, axis):
    sorted_moons = sorted(moons, key=key(axis))
    cursor = 0

    for _key, _moons in groupby(sorted_moons, key=key(axis)):
        _moons = list(_moons)
        for _moon in _moons:
            _moon.speed[axis] += moon_count - len(_moons) - 2 * cursor

        cursor += len(_moons)


def run(moons):
    for axis in range(3):
        _apply_gravity(moons, 4, axis)

    for moon in moons:
        moon.move()


def part_1(text: str, example: bool = False):
    moons = parse(text)
    iterations = 10 if example else 1000
    for _ in range(iterations):
        run(moons)
    result = sum(moon.energy for moon in moons)
    return result


def part_2(text: str, example: bool = False):
    moons = parse(text)
    results = {}
    states = {idx: set() for idx in range(3)}
    counter = 0

    while True:
        for axis in range(3):
            state = hash(
                tuple((moon.position[axis], moon.speed[axis]) for moon in moons)
            )
            if state in states[axis]:
                results.setdefault(axis, counter)

            states[axis].add(state)

        if len(results) == 3:
            break

        run(moons)

        counter += 1

    result = math.lcm(*results.values())
    return result
