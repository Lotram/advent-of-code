from itertools import combinations


def part_1(text, example: bool = False):
    result = 0
    for line in text.strip().split("\n"):
        numbers = list(map(int, line.split()))
        result += max(numbers) - min(numbers)
    return result


def part_2(text, example: bool = False):
    result = 0
    for line in text.strip().split("\n"):
        numbers = list(map(int, line.split()))
        for pair in combinations(numbers, 2):
            if max(pair) % min(pair) == 0:
                result += max(pair) // min(pair)
                continue
    return result
