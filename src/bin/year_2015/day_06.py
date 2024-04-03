import re

pattern = re.compile(
    r"(?P<action>toggle|turn off|turn on) (?P<start_x>\d+),(?P<start_y>\d+) through (?P<end_x>\d+),(?P<end_y>\d+)"
)


def switch(grid, start_x, start_y, end_x, end_y, val):
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            grid[x][y] = not grid[x][y] if val is None else val


values = {"toggle": None, "turn on": True, "turn off": False}


def part_1(text):
    lines = text.strip().split("\n")
    grid = [[False for _ in range(1000)] for _ in range(1000)]
    for line in lines:
        action, *coords = pattern.match(line).groups()
        switch(grid, *map(int, coords), values[action])
    result = sum(1 for line in grid for light in line if light)
    return result


functions = {
    "toggle": lambda x: x + 2,
    "turn off": lambda x: max(0, x - 1),
    "turn on": lambda x: x + 1,
}


def switch_2(grid, start_x, start_y, end_x, end_y, func):
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            grid[x][y] = func(grid[x][y])


def part_2(text):
    lines = text.strip().split("\n")
    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    for line in lines:
        action, *coords = pattern.match(line).groups()
        switch_2(grid, *map(int, coords), functions[action])
    result = sum(light for line in grid for light in line)
    return result
