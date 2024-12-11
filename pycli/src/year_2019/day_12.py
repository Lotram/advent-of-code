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

    def hash(self):
        return hash((tuple(self.position), tuple(self.speed)))


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


def _apply_gravity(moons, moon_count, axis):
    for moon in moons:
        moon.speed[axis] += sum(
            1 for _moon in moons if moon.position[axis] < _moon.position[axis]
        )
        moon.speed[axis] -= sum(
            1 for _moon in moons if moon.position[axis] > _moon.position[axis]
        )


def apply_gravity(moons, moon_count):
    for axis in range(3):
        _apply_gravity(moons, moon_count, axis)


def part_1(text: str, example: bool = False):
    moons = parse(text)
    moon_count = len(moons)
    iterations = 10 if example else 1000
    for _ in range(iterations):
        apply_gravity(moons, moon_count)

        for moon in moons:
            moon.move()

    result = sum(moon.energy for moon in moons)
    return result


def get_state(moons):
    return hash(tuple(moon.hash() for moon in moons))


def part_2(text: str, example: bool = False):
    moons = parse(text)
    moon_count = len(moons)
    states = set()
    while True:
        apply_gravity(moons, moon_count)

        for moon in moons:
            moon.move()

        state = get_state(moons)
        if state in states:
            break
        states.add(state)

    result = len(states)
    return result
