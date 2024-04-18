from collections import defaultdict
from operator import methodcaller


def part_1(text, example: bool = False):
    instruction_blocks = text.strip().split("\n\n")
    state = instruction_blocks[0].split("\n")[0][-2]
    steps = int(instruction_blocks[0].split("\n")[1].split()[-2])
    tape = defaultdict(bool)
    cursor = 0
    instructions = {
        chr(char): {
            False: {
                "write": "1" in instructions[2],
                "move_right": "right" in instructions[3],
                "next_state": instructions[4][-2],
            },
            True: {
                "write": "1" in instructions[6],
                "move_right": "right" in instructions[7],
                "next_state": instructions[8][-2],
            },
        }
        for char, instructions in enumerate(
            map(methodcaller("split", "\n"), instruction_blocks[1:]), start=ord("A")
        )
    }
    for _ in range(steps):
        value = tape[cursor]
        instruction_set = instructions[state][value]
        tape[cursor] = instruction_set["write"]
        cursor += 1 if instruction_set["move_right"] else -1
        state = instruction_set["next_state"]

    result = sum(tape.values())
    return result


def part_2(text, example: bool = False):
    result = None
    return result
