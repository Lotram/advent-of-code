import re
from operator import methodcaller

pattern = re.compile(r"\d+ \w+")

max_values = {
    "blue": 14,
    "green": 13,
    "red": 12,
}


def part_1(lines):
    total = 0
    for line in lines.strip().split("\n"):
        game, draws = line.split(":")
        game_id = int(game.split()[1])
        if all(
            int(value) <= max_values[color]
            for value, color in map(methodcaller("split", " "), pattern.findall(draws))
        ):
            total += game_id
    print(total)


def part_2(lines):
    result = None
    print(result)
