from itertools import product

from .intcode import IntCodeComputer


def part_1(text, example: bool = False):
    computer = IntCodeComputer.from_text(text)
    computer.codes[1] = 12
    computer.codes[2] = 2
    computer.run()
    result = computer.codes[0]
    return result


def part_2(text, example: bool = False):
    initial_values = list(map(int, text.strip().split(",")))
    for i, j in product(range(100), repeat=2):
        computer = IntCodeComputer(codes=initial_values.copy())
        computer.codes[1] = i
        computer.codes[2] = j
        try:
            computer.run()
        except ValueError:
            continue
        if computer.codes[0] == 19690720:
            return computer.codes[1] * 100 + computer.codes[2]
    else:
        raise ValueError("no solution found")