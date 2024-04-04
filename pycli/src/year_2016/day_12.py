def solution(text, registers):
    cursor = 0

    def get_value(x):
        return int(x) if x.isdigit() else registers[x]

    lines = [line.split() for line in text.strip().split("\n")]
    while cursor < len(lines):
        line = lines[cursor]
        match line:
            case ["cpy", x, y]:
                registers[y] = get_value(x)

            case ["inc", x]:
                registers[x] += 1

            case ["dec", x]:
                registers[x] -= 1

            case ["jnz", x, y]:
                if get_value(x) != 0:
                    cursor += int(y)
                    continue

        cursor += 1

    result = registers["a"]
    return result


def part_1(text, example: bool = False):
    registers = dict.fromkeys("abcd", 0)
    return solution(text, registers)


def part_2(text, example: bool = False):
    registers = dict.fromkeys("abcd", 0)
    registers["c"] = 1
    return solution(text, registers)
