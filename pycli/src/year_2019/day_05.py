from .intcode import IntCodeComputer


def part_1(text, example: bool = False):
    computer = IntCodeComputer.from_text(text)
    computer.put(1)
    computer.run()

    result = computer.get_all()[-1]
    return result


def part_2(text, example: bool = False):
    computer = IntCodeComputer.from_text(text)
    computer.put(5)
    computer.run()

    result = computer.get_all()[-1]
    return result
