from itertools import product


def parse(text):
    keys = []
    locks = []
    for schematic in text.strip().split("\n\n"):
        lines = schematic.splitlines()
        assert len(lines) == 7 and all(len(line) == 5 for line in lines)
        value = tuple(column.count("#") for column in zip(*lines))
        if all(char == "#" for char in schematic[0]):
            locks.append(value)
        else:
            keys.append(value)
    return keys, locks


def part_1(text, example: bool = False):
    keys, locks = parse(text)
    result = sum(
        all(k + l <= 7 for k, l in zip(key, lock)) for key, lock in product(keys, locks)
    )
    return result


def part_2(text, example: bool = False):
    result = None
    return result
