import math
from itertools import combinations


def part_1(text):
    weights = list(map(int, text.strip().split("\n")))
    target = sum(weights) // 3
    result = float("inf")
    for number in range(1, len(weights) // 3 + 1):
        for _weights in combinations(weights, number):
            if sum(_weights) == target:
                result = min(result, math.prod(_weights))
        if result < float("inf"):
            break
    return result


def part_2(text):
    weights = list(map(int, text.strip().split("\n")))
    target = sum(weights) // 4
    result = float("inf")
    for number in range(1, len(weights) // 4 + 1):
        for _weights in combinations(weights, number):
            if sum(_weights) == target:
                result = min(result, math.prod(_weights))
        if result < float("inf"):
            break
    return result
