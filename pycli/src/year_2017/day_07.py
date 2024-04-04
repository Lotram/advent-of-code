import re
from collections import Counter
from dataclasses import dataclass
from typing import Self

pattern = re.compile(
    r"(?P<name>\w+) \((?P<size>\d+)\)(?: -> (?P<children>(?:[\w, ])+))?"
)


@dataclass(slots=True)
class Program:
    name: str
    size: int
    children: list[str | Self]
    parent: str | None = None
    _weight: int | None = None

    @property
    def weight(self):
        if self._weight is None:
            self._weight = self.size + sum(child.weight for child in self.children)
        return self._weight


def get_programs(text) -> dict[str, Program]:
    lines = text.strip().split("\n")
    programs = {}
    for line in lines:
        name, size, children = pattern.match(line).groups()
        programs[name] = Program(
            name, int(size), children.split(", ") if children else []
        )

    for program in programs.values():
        for child in program.children:
            programs[child].parent = program

        program.children = [programs[child] for child in program.children]

    root = next(program for program in programs.values() if program.parent is None)
    return root


def part_1(text, example: bool = False):
    root = get_programs(text)
    result = root.name
    return result


def part_2(text, example: bool = False):
    root = get_programs(text)
    current = root
    faulty = None
    while faulty is None:
        counter = Counter(child.weight for child in current.children)
        if len(counter) > 1:
            current = next(
                child
                for child in current.children
                if child.weight == counter.most_common(2)[1][0]
            )
        else:
            faulty = current

    return faulty.size - (
        faulty.weight
        - next(child.weight for child in faulty.parent.children if child != faulty)
    )
