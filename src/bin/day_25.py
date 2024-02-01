import re


def get_idx(row, col):
    return (row + col - 2) * (row + col - 1) // 2 + col


def part_1(text):
    row, column = map(int, re.findall(r"\d+", text.strip()))
    idx = get_idx(row, column)
    return (pow(252533, idx - 1, 33554393) * 20151125) % 33554393


def part_2(text):
    result = None
    return result
