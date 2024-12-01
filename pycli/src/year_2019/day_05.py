from .intcode import IntCodeComputer


def part_1(text, example: bool = False):
    computer = IntCodeComputer.from_text(text)
    computer.input_queue.put(1)
    computer.run()

    while not computer.output_queue.empty():
        result = computer.output_queue.get()

    return result


def part_2(text, example: bool = False):
    computer = IntCodeComputer.from_text(text)
    computer.input_queue.put(5)

    computer.run()

    while not computer.output_queue.empty():
        result = computer.output_queue.get()
    return result
