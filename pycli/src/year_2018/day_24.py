import re
from heapq import nlargest
from itertools import count
from operator import attrgetter
from typing import Literal, Self

from pydantic import BaseModel, Field


weaknesses_and_immunities = r"((\((immune to (?P<immunities>[\w, ]+))?(?:; )?(weak to (?P<weaknesses>[\w, ]+))?\) )|(\((weak to (?P<weaknesses_2>[\w, ]+))?(?:; )?(immune to (?P<immunities_2>[\w, ]+))?\) ))?"
pattern = re.compile(
    rf"(?P<units>\d+) units each with (?P<hit_points>\d+) hit points {weaknesses_and_immunities}with an attack that does (?P<attack>\d+) (?P<attack_type>\w+) damage at initiative (?P<initiative>\d+)"
)


class Group(BaseModel):
    id: int
    units: int
    hit_points: int
    attack: int
    attack_type: str
    initiative: int
    weaknesses: set[str] = set()
    immunities: set[str] = set()
    target: Self | None = Field(None, repr=False)
    type: Literal["immune", "infection"]

    @property
    def effective_power(self):
        return self.attack * self.units


class Army(BaseModel):
    name: Literal["immune", "infection"]
    groups: list[Group]

    def print(self):
        print(self.name)
        for group in self.groups:
            print(f"Group {group.id}: {group.units}")


def parse(text):
    immune_system, infection = text.strip().split("\n\n")
    return (
        Army(groups=parse_army(immune_system, "immune"), name="immune"),
        Army(groups=parse_army(infection, "infection"), name="infection"),
    )


def parse_army(army, type):
    groups = []
    for idx, line in enumerate(army.splitlines()[1:], start=1):
        values = pattern.match(line).groupdict()
        values |= {
            "weaknesses": values["weaknesses"] or values["weaknesses_2"],
            "immunities": values["immunities"] or values["immunities_2"],
            "id": idx,
            "type": type,
        }
        values = {key: value for key, value in values.items() if value is not None}
        if "immunities" in values:
            values["immunities"] = set(values["immunities"].split(", "))
        if "weaknesses" in values:
            values["weaknesses"] = set(values["weaknesses"].split(", "))
        groups.append(Group.model_validate(values))

    return groups


def assign_targets(armies):
    already_assigned = set()
    for group in sorted(
        (group for army in armies for group in army.groups),
        key=attrgetter("effective_power", "initiative"),
        reverse=True,
    ):
        enemy_army = next(army for army in armies if group.type != army.name)
        try:
            group.target = nlargest(
                1,
                (
                    enemy
                    for enemy in enemy_army.groups
                    if group.attack_type not in enemy.immunities
                    and (enemy_army.name, enemy.id) not in already_assigned
                ),
                key=lambda enemy: (
                    group.attack_type in enemy.weaknesses,
                    enemy.effective_power,
                    enemy.initiative,
                ),
            )[0]
            already_assigned.add((enemy_army.name, group.target.id))
        except IndexError:
            group.target = None


def attack(armies):
    for group in sorted(
        (group for army in armies for group in army.groups),
        key=attrgetter("initiative"),
        reverse=True,
    ):
        if (target := group.target) is None:
            continue

        group.target = None
        if group.units <= 0:
            continue

        damages = group.effective_power
        if group.attack_type in target.weaknesses:
            damages *= 2
        # print(f"{group.type} group {group.id} attacks {target.type} {target.id}")
        # print(
        #     f"damages: {damages}, killed units: {min(target.units, damages // target.hit_points)}"
        # )

        target.units -= min(target.units, damages // target.hit_points)


def run(armies):
    i = 0
    prev_state = None
    while True:
        assign_targets(armies)
        attack(armies)
        for army in armies:
            army.groups = [group for group in army.groups if group.units > 0]
            if not army.groups:
                other_army = next(army_ for army_ in armies if army_.name != army.name)
                return sum(
                    group.units for group in other_army.groups
                ), other_army.name == "immune"
        i += 1
        state = tuple(tuple(group.units for group in army.groups) for army in armies)
        if state == prev_state:
            return -1, False
        prev_state = state


def part_1(text, example: bool = False):
    armies = parse(text)
    return run(armies)[0]


def part_2(text, example: bool = False):
    counter = count(110)

    for value in counter:
        armies = parse(text)
        immune_system = next(army for army in armies if army.name == "immune")
        for group in immune_system.groups:
            group.attack += value

        result, immune_won = run(armies)
        if immune_won:
            return result
