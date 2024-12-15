from itertools import product

from .intcode import ListIntCodeComputer


def part_1(text, example: bool = False):
    computer = ListIntCodeComputer.from_text(text)
    computer.memory[1] = 12
    computer.memory[2] = 2
    computer.run()
    result = computer.memory[0]
    return result


def part_2(text, example: bool = False):
    computer = ListIntCodeComputer.from_text(text)
    for i, j in product(range(100), repeat=2):
        computer.reset()
        computer.memory[1] = i
        computer.memory[2] = j
        try:
            computer.run()
        except ValueError:
            continue
        if computer.memory[0] == 19690720:
            return computer.memory[1] * 100 + computer.memory[2]
    else:
        raise ValueError("no solution found")
