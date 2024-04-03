import random
from operator import methodcaller
from string import ascii_uppercase


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    transformations = lines[:-2]
    molecule = lines[-1]
    possibilities = set()
    for transformation in transformations:
        before, after = transformation.split(" => ")
        split = molecule.split(before)
        for idx in range(len(split) - 1):
            possibility = split[0] + "".join(
                f"{after if idx == _idx else before}{part}"
                for _idx, part in enumerate(split[1:])
            )
            possibilities.add(possibility)
    return len(possibilities)


def sort_key(transformation):
    before, after = transformation
    return len([char for char in after if char in ascii_uppercase]) - len(
        [char for char in before if char in ascii_uppercase]
    )


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    result = 0

    transformations = sorted(
        map(methodcaller("split", " => "), lines[:-2]), key=sort_key, reverse=True
    )

    molecule = lines[-1]
    while molecule != "e":
        for before, after in transformations:
            if _count := molecule.count(after):
                result += _count
                molecule = molecule.replace(after, before)
                break
        else:
            result = 0
            random.shuffle(transformations)
            molecule = lines[-1]
            transformations = sorted(transformations, key=sort_key, reverse=True)

    return result
