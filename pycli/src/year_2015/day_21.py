from itertools import combinations, product
from math import ceil
from typing import NamedTuple


class Equipment(NamedTuple):
    price: int
    dammage: int
    armor: int


weapons = [
    Equipment(8, 4, 0),
    Equipment(10, 5, 0),
    Equipment(25, 6, 0),
    Equipment(40, 7, 0),
    Equipment(74, 8, 0),
]

armors = [
    Equipment(0, 0, 0),
    Equipment(13, 0, 1),
    Equipment(31, 0, 2),
    Equipment(53, 0, 3),
    Equipment(75, 0, 4),
    Equipment(102, 0, 5),
]

rings = [
    Equipment(0, 0, 0),
    Equipment(0, 0, 0),
    Equipment(25, 1, 0),
    Equipment(50, 2, 0),
    Equipment(100, 3, 0),
    Equipment(20, 0, 1),
    Equipment(40, 0, 2),
    Equipment(80, 0, 3),
]


def add(*items):
    return Equipment(*map(sum, zip(*items)))


def part_1(text, example: bool = False):
    boss_hp, boss_damage, boss_armor = [
        int(line.split(": ")[1]) for line in text.strip().split("\n")
    ]
    player_hp = 100
    candidates = (
        Equipment(*map(sum, zip(weapon, armor, ring_1, ring_2)))
        for weapon, armor, (ring_1, ring_2) in product(
            weapons, armors, combinations(rings, 2)
        )
    )
    result = min(
        price
        for (price, dammage, armor) in candidates
        if ceil(boss_hp / max(1, dammage - boss_armor))
        <= ceil(player_hp / max(boss_damage - armor, 1))
    )
    return result


def part_2(text, example: bool = False):
    boss_hp, boss_damage, boss_armor = [
        int(line.split(": ")[1]) for line in text.strip().split("\n")
    ]
    player_hp = 100
    candidates = (
        Equipment(*map(sum, zip(weapon, armor, ring_1, ring_2)))
        for weapon, armor, (ring_1, ring_2) in product(
            weapons, armors, combinations(rings, 2)
        )
    )

    result = max(
        price
        for (price, dammage, armor) in candidates
        if ceil(boss_hp / max(1, dammage - boss_armor))
        > ceil(player_hp / max(boss_damage - armor, 1))
    )
    return result
