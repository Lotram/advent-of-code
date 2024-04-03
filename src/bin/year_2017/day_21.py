from itertools import batched

import numpy as np

from .grid import Grid

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


def join_subs(subs: list[np.ndarray], size: int) -> np.ndarray:
    return np.concatenate(
        list(np.concatenate(batch, axis=1) for batch in batched(subs, size // 2))
    )


def part_1(text):
    arr = np.array([list(line) for line in pattern])
    for _ in range(5):
        subarrays = list(get_subarrays(arr, len(arr)))
    result = None
    return result


def part_2(text):
    result = None
    return result
