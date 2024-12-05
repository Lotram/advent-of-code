from .intcode import IntCodeComputer


def part_1(text, example: bool = False):
    computer = IntCodeComputer.from_text(text)
    computer.put(1)
    computer.run()
    result = computer.get()
    return result


def part_2(text, example: bool = False):
    computer = IntCodeComputer.from_text(text)
    computer.put(2)
    computer.run()
    result = computer.get()
    return result
