import math
from itertools import product
from typing import NamedTuple

DAMAGE = 9
BOSS_HP = 58


class Spells(NamedTuple):
    poison: int
    missile: int
    drain: int
    hard: bool
    shield: int = 0
    recharge: int = 0

    @property
    def total_damage(self):
        return self.poison * 18 + self.missile * 4 + self.drain * 2

    @property
    def turn_count(self):
        return self.poison + self.missile + self.drain + self.shield + self.recharge

    @property
    def mana(self):
        return (
            173 * self.poison
            + 53 * self.missile
            + 73 * self.drain
            + 113 * self.shield
            + 229 * self.recharge
        )

    @property
    def feasible(self):
        return (
            self.poison <= math.floor(self.turn_count / 3)
            and self.shield <= math.floor(self.turn_count / 3)
            and self.recharge <= math.floor(self.turn_count / 3)
        )

    @property
    def has_enough_hp(self):
        return (
            50 + 7 * 3 * self.shield + 2 * self.drain
            >= (self.turn_count - 1) * DAMAGE + (self.hard is True) * self.turn_count
        )

    @property
    def has_enough_mana(self):
        return 500 + 505 * self.recharge >= self.mana

    @property
    def does_enough_damage(self):
        return self.total_damage >= BOSS_HP

    @property
    def valid(self):
        return (
            self.feasible
            and self.has_enough_hp
            and self.has_enough_mana
            and self.does_enough_damage
        )


def get_candidates(hard=False):
    """
    Generating all candidates is fast, as there are not that many options
    """
    max_poisons = range(math.floor(BOSS_HP / 18) + 1)
    max_missiles = range(math.floor(BOSS_HP / 4) + 1)
    max_drain = range(math.floor(BOSS_HP / 2) + 1)
    max_shield = range(6)  # arbitrary value
    max_recharge = range(6)  # arbitrary value
    for poison, missile, drain, shield, recharge in product(
        max_poisons, max_missiles, max_drain, max_shield, max_recharge
    ):
        candidate = Spells(
            poison=poison,
            missile=missile,
            drain=drain,
            shield=shield,
            recharge=recharge,
            hard=hard,
        )
        if candidate.valid:
            yield candidate


def part_1(text, example: bool = False):
    result = min(candidate.mana for candidate in get_candidates())

    return result


def part_2(text, example: bool = False):
    result = min(candidate.mana for candidate in get_candidates(hard=True))

    return result
