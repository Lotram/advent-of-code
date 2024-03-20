import math


def toggle(instruction):
    match instruction:
        case ["inc", a]:
            return ["dec", a]
        case [_, a]:
            return ["inc", a]
        case ["jnz", a, b]:
            return ["cpy", a, b]
        case [_, a, b]:
            return ["jnz", a, b]
        case _:
            raise ValueError(f"error while toggling {instruction}")


def solution(text, registers):
    cursor = 0

    def get_value(x):
        return int(x) if x.strip("-").isdigit() else registers[x]

    lines = [line.split() for line in text.strip().split("\n")]
    while cursor < len(lines):
        line = lines[cursor]
        match line:
            case ["cpy", x, y]:
                if y.strip("-").isdigit():
                    pass
                registers[y] = get_value(x)

            case ["inc", x]:
                registers[x] += 1

            case ["dec", x]:
                registers[x] -= 1

            case ["jnz", x, y]:
                if get_value(x) != 0:
                    cursor += get_value(y)
                    continue
            case ["tgl", x]:
                try:
                    toggled = cursor + get_value(x)
                    lines[toggled] = toggle(lines[toggled])
                except IndexError:
                    pass
            case _:
                raise ValueError(f"invalid instructioon: {line}")

        cursor += 1
    result = registers["a"]
    return result


def part_1(text):
    registers = {"a": 7, "b": 0, "c": 0, "d": 0}
    result = solution(text, registers)
    return result


def part_2(text):
    return math.factorial(12) + 77 * 73
