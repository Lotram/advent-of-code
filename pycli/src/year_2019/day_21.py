from pycli.src.year_2019.intcode import ListIntCodeComputer


def print_outputs(outputs):
    print("".join(chr(c) if c <= 256 else str(c) for c in outputs))


def part_1(text, example: bool = False):
    computer = ListIntCodeComputer.from_text(text)

    # J = D AND NOT (A AND B AND C)
    instructions = [
        "OR A T",
        "AND B T",
        "AND C T",
        "NOT T J",
        "AND D J",
    ]

    instructions.append("WALK")
    for char in map(ord, "\n".join(instructions)):
        computer.put(char)
    computer.put(10)
    computer.run()
    outputs = computer.get_all()
    return outputs[-1]


def part_2(text, example: bool = False):
    computer = ListIntCodeComputer.from_text(text)

    # J = D AND NOT (A AND B AND C) AND (H AND E AND (I OR F))
    instructions = [
        "OR A T",
        "AND B T",
        "AND C T",
        "NOT T J",
        "AND D J",
        "NOT D T",
        "OR I T",
        "OR F T",
        "AND E T",
        "OR H T",
        "AND T J",
    ]

    instructions.append("RUN")
    for char in map(ord, "\n".join(instructions)):
        computer.put(char)
    computer.put(10)
    computer.run()
    outputs = computer.get_all()
    return outputs[-1]
