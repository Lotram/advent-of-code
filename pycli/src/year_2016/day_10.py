import re
from collections import deque
from typing import NamedTuple


VALUES = re.compile(r"value (?P<value>\d+) goes to (?P<bot>bot \d+)")
TARGETS = re.compile(r"((?:bot|output) \d+)")


class Microchip(NamedTuple):
    value: int
    target: str


class Output(NamedTuple):
    id: str
    chips: set


class Bot(NamedTuple):
    id: str
    chips: set
    low: str
    high: str


def part_1(text, example: bool = False):
    chips = deque()
    targets = {}
    for line in text.strip().split("\n"):
        if line.startswith("value"):
            value, bot = VALUES.match(line).groups()
            chips.append(Microchip(int(value), bot))
        else:
            bot, low, high = TARGETS.findall(line)
            targets[bot] = Bot(bot, set(), low, high)

    while chips:
        chip = chips.popleft()

        target = targets.setdefault(chip.target, Output(chip.target, set()))
        target.chips.add(chip.value)
        if isinstance(target, Output):
            continue

        target.chips.add(chip.value)
        if target.chips == {17, 61}:
            return target.id.split()[1]

        if len(target.chips) == 2:
            low, high = sorted(target.chips)
            chips.append(Microchip(low, target.low))
            chips.append(Microchip(high, target.high))

    result = None
    return result


def part_2(text, example: bool = False):
    chips = deque()
    targets = {}
    for line in text.strip().split("\n"):
        if line.startswith("value"):
            value, bot = VALUES.match(line).groups()
            chips.append(Microchip(int(value), bot))
        else:
            bot, low, high = TARGETS.findall(line)
            targets[bot] = Bot(bot, set(), low, high)

    while chips:
        chip = chips.popleft()

        target = targets.setdefault(chip.target, Output(chip.target, set()))
        target.chips.add(chip.value)
        if isinstance(target, Output):
            continue

        target.chips.add(chip.value)

        if len(target.chips) == 2:
            low, high = sorted(target.chips)
            chips.append(Microchip(low, target.low))
            chips.append(Microchip(high, target.high))

    result = (
        targets["output 0"].chips.pop()
        * targets["output 1"].chips.pop()
        * targets["output 2"].chips.pop()
    )
    return result
