import math

import numpy as np


PATTERN = [0, 1, 0, -1]


def f(i, j):
    return PATTERN[((i + 1) // (j + 1)) % 4]


def func(item):
    return abs(item) % 10


def run_phase(signal):
    return [
        abs(sum(digit * f(i, j) for i, digit in enumerate(signal))) % 10
        for j in range(len(signal))
    ]


def part_1(text, example: bool = False):
    phase_count = 100
    signal = np.array(list(map(int, text.strip())))
    size = len(signal)
    P = np.array([[f(i, j) for i in range(size)] for j in range(size)])

    for _ in range(phase_count):
        signal = func(np.matmul(P, signal))

    result = "".join(map(str, signal[:8]))
    return result


def run_phase_2(signal):
    new_signal = []
    value = 0
    for j in range(len(signal) - 1, -1, -1):
        value += signal[j]
        new_signal.append(value % 10)

    return list(reversed(new_signal))


def g(k, n):
    return math.comb(k + n - 2, k - 1) % 10


def part_2(text, example: bool = False):
    phase_count = 100
    repeated = 10_000
    signal = list(map(int, text.strip())) * repeated
    offset = int("".join(map(str, signal[:7])))
    signal = list(signal[offset:])
    for _ in range(phase_count):
        signal = run_phase_2(signal)

    result = "".join(map(str, signal[:8]))
    return result
