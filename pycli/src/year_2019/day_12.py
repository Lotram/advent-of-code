import re
from collections import defaultdict
from collections.abc import Callable
from copy import deepcopy
from itertools import combinations, groupby
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


def func(moons, iterations):
    moons = deepcopy(moons)
    for _ in range(iterations):
        apply_gravity(moons, len(moons))

        for moon in moons:
            moon.move()

    return {moon.idx: moon.hash() for moon in moons}


def part_2(text: str, example: bool = False):
    moons = parse(text)
    moon_count = len(moons)
    states = {idx: {} for idx in range(moon_count)}
    counter = 0
    matched = {}
    while True:
        for moon in moons:
            if moon.hash() in states[moon.idx]:
                loop_start = states[moon.idx][moon.hash()]
                loop_size = counter - loop_start
                matched.setdefault(moon.idx, (loop_start, loop_size))

            states[moon.idx][moon.hash()] = counter
        apply_gravity(moons, moon_count)

        for moon in moons:
            moon.move()

        counter += 1
        if counter >= 2790:
            break

    breakpoint()
    result = len(states)
    return result


results = {0: [24, 120, 8], 1: [24, 48, 80], 2: [120, 48, 48], 3: [8, 80, 48]}
"""
sympy.factorint(4686774924)
{2: 2, 3: 1, 13: 2, 983: 1, 2351: 1}

sympy.factorint(2772)
{2: 2, 3: 2, 7: 1, 11: 1}

[(4, 252), (26, 252), (6, 616), (0, 924)]
"""


# def part_2(text: str, example: bool = False):
#     all_moons = parse(text)
#     results = defaultdict(list)
#     for x, y in combinations(all_moons, r=2):
#         moons = deepcopy([x, y])
#         states = {}
#         counter = 0
#         loop_size = None
#         loop_start = None
#         while True:
#             state = get_state(moons)
#             if state in states:
#                 assert state == get_state([x, y])
#                 loop_start = states[state]
#                 loop_size = counter - loop_start
#                 break

#             states[state] = counter

#             apply_gravity(moons, 2)

#             for moon in moons:
#                 moon.move()

#             counter += 1

#         _result = (loop_start, loop_size)
#         print(_result)
#         results[x.idx].append(_result)
#         results[y.idx].append(_result)

#     breakpoint()
#     result = None
#     return result
