import math
from itertools import combinations


def solution(text, group_count):
    weights = list(map(int, text.strip().split("\n")))
    target = sum(weights) // group_count
    result = float("inf")
    for number in range(1, len(weights) // group_count + 1):
        for _weights in combinations(weights, number):
            if sum(_weights) == target:
                result = min(result, math.prod(_weights))
        if result < float("inf"):
            break
    return result


def part_1(text, example: bool = False):
    return solution(text, 3)


def part_2(text, example: bool = False):
    return solution(text, 4)
