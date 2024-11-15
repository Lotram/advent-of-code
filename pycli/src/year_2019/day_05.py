from .intcode import IntCodeComputer


def part_1(text, example: bool = False):
    computer = IntCodeComputer.from_text(text)
    outputs = computer.run(inputs=[1])
    result = outputs[-1]
    return result


def part_2(text, example: bool = False):
    computer = IntCodeComputer.from_text(text)
    outputs = computer.run(inputs=[5])
    result = outputs[-1]
    return result
