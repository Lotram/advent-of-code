from .intcode import ListIntCodeComputer


def part_1(text, example: bool = False):
    computer = ListIntCodeComputer.from_text(text)
    computer.put(1)
    computer.run()
    result = computer.get()
    return result


def part_2(text, example: bool = False):
    computer = ListIntCodeComputer.from_text(text)
    computer.put(2)
    computer.run()
    result = computer.get()
    return result
