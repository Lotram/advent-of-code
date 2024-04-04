from operator import eq, gt, lt, methodcaller

data = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    for idx, line in enumerate(lines, start=1):
        args = line.split(":", maxsplit=1)[1].split(", ")
        if all(
            data[key.strip()] == int(value)
            for key, value in map(methodcaller("split", ":"), args)
        ):
            return idx


op = {
    "children": eq,
    "cats": gt,
    "samoyeds": eq,
    "pomeranians": lt,
    "akitas": eq,
    "vizslas": eq,
    "goldfish": lt,
    "trees": gt,
    "cars": eq,
    "perfumes": eq,
}


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    for idx, line in enumerate(lines, start=1):
        args = line.split(":", maxsplit=1)[1].split(", ")
        if all(
            op[key.strip()](int(value), data[key.strip()])
            for key, value in map(methodcaller("split", ":"), args)
        ):
            return idx
