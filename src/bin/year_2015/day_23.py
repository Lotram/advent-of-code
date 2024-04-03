def solution(instructions, registers):
    cursor = 0
    while cursor < len(instructions):
        match instructions[cursor]:
            case ["hlf", register]:
                if registers[register] % 2:
                    raise ValueError("register is not even", registers, register)
                registers[register] //= 2
                cursor += 1

            case ["tpl", register]:
                registers[register] *= 3
                cursor += 1

            case ["inc", register]:
                registers[register] += 1
                cursor += 1

            case ["jmp", offset]:
                cursor += int(offset)

            case ["jie", register, offset]:
                register = register.strip(",")
                if registers[register] % 2 == 0:
                    cursor += int(offset)
                else:
                    cursor += 1

            case ["jio", register, offset]:
                register = register.strip(",")
                if registers[register] == 1:
                    cursor += int(offset)
                else:
                    cursor += 1

    result = registers["b"]
    return result


def part_1(text, example: bool = False):
    # input looks like https://fr.wikipedia.org/wiki/Conjecture_de_Syracuse
    instructions = [line.split() for line in text.strip().split("\n")]
    registers = {"a": 0, "b": 0}
    return solution(instructions, registers)


def part_2(text, example: bool = False):
    instructions = [line.split() for line in text.strip().split("\n")]
    registers = {"a": 1, "b": 0}
    return solution(instructions, registers)
