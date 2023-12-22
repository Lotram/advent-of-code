import re
from functools import cache
from itertools import repeat

pattern = re.compile(r"\.+")


@cache
def solve(blocks, values):
    if not blocks:
        return int(not bool(values))

    if not values:
        return int(not any("#" in block for block in blocks))

    block = blocks[0]
    value = values[0]
    if len(blocks[0]) < value:
        if "#" in blocks[0]:
            return 0
        return solve(blocks[1:], values)

    if len(block) > value and block[value] == "#":
        if block[0] == "#":
            return 0

        res = solve((block[1:],) + blocks[1:], values)
        return res

    remain = (block[value + 1 :],) + blocks[1:]
    res_remain = solve(remain, values[1:])
    if block[0] == "#":
        return res_remain

    res_increment = solve((block[1:],) + blocks[1:], values)

    return res_remain + res_increment


def parse_line(line):
    symbols, values = line.split(" ")
    symbols = pattern.sub(r".", symbols).strip(".")
    values = tuple(map(int, values.split(",")))
    return tuple(symbols.split(".")), values


def part_1(text):
    lines = text.strip(".").split("\n")
    counter = 0
    for line in lines:
        blocks, values = parse_line(line)
        line_counter = solve(blocks, values)
        counter += line_counter
    print(counter)


def parse_line_2(line):
    symbols, values = line.split()
    symbols = "?".join(repeat(symbols, 5))
    values = ",".join(repeat(values, 5))
    symbols = pattern.sub(r".", symbols.strip("."))
    values = tuple(map(int, values.split(",")))
    return tuple(symbols.split(".")), values


def part_2(text):
    lines = [line for line in text.strip(".").split("\n") if line]
    counter = 0
    for line in lines:
        blocks, values = parse_line_2(line)
        line_counter = solve(blocks, values)
        counter += line_counter
    print(counter)
