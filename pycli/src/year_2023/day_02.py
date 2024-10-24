import re
from operator import methodcaller


pattern = re.compile(r"\d+ \w+")

max_values = {
    "blue": 14,
    "green": 13,
    "red": 12,
}


def part_1(text, example=False):
    lines = text.strip().split("\n")
    total = 0
    for game_id, line in enumerate(lines, 1):
        _, draws = line.split(":")
        if all(
            int(value) <= max_values[color]
            for value, color in map(methodcaller("split", " "), pattern.findall(draws))
        ):
            total += game_id
    return total


def part_2(text, example=False):
    lines = text.strip().split("\n")
    total = 0
    for line in lines:
        _, draws = line.split(":")
        values = {"red": [], "green": [], "blue": []}
        for value, color in map(methodcaller("split", " "), pattern.findall(draws)):
            values[color].append(int(value))

        total += max(values["red"]) * max(values["green"]) * max(values["blue"])
    return total
