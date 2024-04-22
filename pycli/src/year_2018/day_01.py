from itertools import cycle


def part_1(text, example: bool = False):
    result = sum(map(int, text.strip().split("\n")))
    return result


def part_2(text, example: bool = False):
    result = 0
    seen = {result}
    for frequency in cycle(map(int, text.strip().split("\n"))):
        result += frequency
        if result in seen:
            break
        seen.add(result)

    return result
