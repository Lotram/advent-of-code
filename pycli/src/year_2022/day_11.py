import heapq
import math
import re
from collections import deque
from collections.abc import Callable
from functools import cache
from operator import attrgetter, methodcaller

from pydantic import BaseModel


int_pattern = re.compile(r"\d+")


class Monkey(BaseModel):
    idx: int
    items: deque[int]
    operation: Callable[[int], int]
    divisible_by: int
    if_true: int
    if_false: int
    counter: int = 0

    @cache
    def get_next(self, item, part):
        _item = self.operation(item)
        if part == 1:
            _item = int(_item / 3)

        return _item, self.if_true if _item % self.divisible_by == 0 else self.if_false

    def __hash__(self) -> int:
        return hash(self.idx)


class Monkeys(BaseModel):
    monkeys: list[Monkey]

    def process_items(self, part, rounds):
        lcm = math.lcm(*[monkey.divisible_by for monkey in self.monkeys])
        for _monkey in self.monkeys:
            for _item in _monkey.items:
                monkey = _monkey
                item = _item
                _rounds = 0
                while _rounds < rounds:
                    monkey.counter += 1
                    item, monkey_idx = monkey.get_next(item, part)
                    item %= lcm
                    if monkey_idx < monkey.idx:
                        _rounds += 1
                    monkey = self.monkeys[monkey_idx]

    def monkey_business(self):
        return math.prod(heapq.nlargest(2, map(attrgetter("counter"), self.monkeys)))


def parse(text):
    monkey_data = text.strip().split("\n\n")
    monkeys = []
    for idx, data in enumerate(map(methodcaller("split", "\n"), monkey_data)):
        monkeys.append(
            Monkey(
                idx=idx,
                items=data[1].strip().removeprefix("Starting items: ").split(", "),
                operation=eval(
                    data[2].strip().replace("Operation: new =", "lambda old:")
                ),
                divisible_by=int_pattern.search(data[3]).group(),
                if_true=int_pattern.search(data[4]).group(),
                if_false=int_pattern.search(data[5]).group(),
            )
        )
    return Monkeys(monkeys=monkeys)


def _solution(text, part):
    rounds = 20 if part == 1 else 10_000
    monkeys = parse(text)
    monkeys.process_items(part=part, rounds=rounds)
    return monkeys.monkey_business()


def part_1(text, example: bool = False):
    return _solution(text, part=1)


def part_2(text, example: bool = False):
    return _solution(text, part=2)
