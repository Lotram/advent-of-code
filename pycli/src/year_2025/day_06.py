from itertools import zip_longest
from math import prod
from operator import methodcaller


operators = {"*": prod, "+": sum}


def part_1(text, example: bool = False):
    problems = list(zip(*map(methodcaller("split"), text.splitlines())))
    result = 0
    for *values, op in problems:
        result += operators[op](map(int, values))

    return result


def part_2(text, example: bool = False):
    rows = [list(line) for line in text.splitlines()]
    columns = list(zip_longest(*rows, fillvalue=" "))
    numbers = []
    result = 0
    op = None
    for column in columns:
        if all(value == " " for value in column):
            result += op(numbers)
            numbers = []
            continue

        numbers.append(int("".join(column[:-1]).strip()))
        if column[-1] != " ":
            op = operators[column[-1]]

    result += op(numbers)
    return result
