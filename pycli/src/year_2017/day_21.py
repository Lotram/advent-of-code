import math
from itertools import batched

import numpy as np


pattern = """.#.
..#
###"""


def get_subarrays(arr: np.ndarray, size: int) -> list[np.ndarray]:
    sub_size = 2 if size % 2 == 0 else 3
    return [
        arr[row : row + sub_size, col : col + sub_size]
        for row in range(0, size, sub_size)
        for col in range(0, size, sub_size)
    ]


def join_subs(subs: list[np.ndarray]) -> np.ndarray:
    size = int(math.sqrt(len(subs)))
    return np.concatenate(
        list(np.concatenate(batch, axis=1) for batch in batched(subs, size))
    )


def hash_array(arr):
    return tuple(arr.flatten())


def parse_rules(text):
    hashed_rules = {}
    for line in text.strip().split("\n"):
        _in, _out = line.split(" => ")
        in_ = np.array([list(line_) for line_ in _in.split("/")])
        out = np.array([list(line_) for line_ in _out.split("/")])
        for k in range(4):
            hashed_rules[hash_array(np.rot90(in_, k))] = out
            hashed_rules[hash_array(np.flip(np.rot90(in_, k), axis=0))] = out
    return hashed_rules


def solve(text, iterations):
    hashed_rules = parse_rules(text)
    arr = np.array([list(line) for line in pattern.split("\n")])
    for _ in range(iterations):
        subs = get_subarrays(arr, len(arr))
        arr = join_subs(list(hashed_rules[hash_array(sub)] for sub in subs))
    result = np.sum(arr == "#")
    return result


def part_1(text, example: bool = False):
    return solve(text, iterations=2 if example else 5)


def part_2(text, example: bool = False):
    return solve(text, iterations=2 if example else 18)
