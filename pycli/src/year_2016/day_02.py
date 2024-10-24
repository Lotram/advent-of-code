from pycli.src.grid import EAST, NORTH, SOUTH, WEST, Grid, Vector


DIRECTIONS = {"U": NORTH, "L": WEST, "D": SOUTH, "R": EAST}


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    position = Vector(1, 1)
    code = []
    keypad = Grid(arr=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    for line in lines:
        for char in line:
            if keypad.contains(new_position := (position + DIRECTIONS[char])):
                position = new_position
        code.append(keypad[position])
    result = "".join(map(str, code))
    return result


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    position = Vector(1, 1)
    code = []
    keypad = Grid(
        arr=[
            ["0", "0", "1", "0", "0"],
            ["0", "2", "3", "4", "0"],
            ["5", "6", "7", "8", "9"],
            ["0", "A", "B", "C", "0"],
            ["0", "0", "D", "0", "0"],
        ]
    )
    for line in lines:
        for char in line:
            if (
                keypad.contains(new_position := (position + DIRECTIONS[char]))
                and keypad[new_position] != "0"
            ):
                position = new_position
        code.append(keypad[position])
    result = "".join(code)
    return result
