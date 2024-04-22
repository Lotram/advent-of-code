from collections import Counter
from itertools import product


def part_1(text, example: bool = False):
    twos = 0
    threes = 0
    for line in text.strip().split("\n"):
        values = set(Counter(line).values())
        if 2 in values:
            twos += 1
        if 3 in values:
            threes += 1

    result = twos * threes
    return result


def part_2(text, example: bool = False):
    for line, other in product(text.strip().split("\n"), repeat=2):
        single_diff = False
        result = []
        for c, o in zip(line, other):
            if c != o:
                if single_diff:
                    break
                single_diff = True
            else:
                result.append(c)
        else:
            if single_diff:
                return "".join(result)
