def _solution(lines, registers):
    cursor = 0
    loops = 0

    def get_value(x):
        return int(x) if x.isdigit() else registers[x]

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
            case ["out", x]:
                print(registers[x], end="")
                loops += 1
                if loops >= 20:
                    return ""

        cursor += 1

    result = registers
    return result


def solution(x):
    """
    get the first int greater than x and written as "101010...10", and returns its
    substraction by x
    """
    result = 2
    while result < x:
        result = (result << 2) + 2
    return result - x


def part_1(text, example: bool = False):
    """
    The set of instructions is equivalent to:

    while True:
        a = value + seed
        while a:
            a, b = a // 2, a % 2
            print(b, end="")


    where seed depends on the input and value is the initial value of a
    """
    lines = [line.split() for line in text.strip().split("\n")[:3]]
    seed = int(lines[1][1]) * int(lines[2][1])
    return solution(seed)


def f(x):
    loops = 0
    while True:
        a = x
        while a:
            a, b = a // 2, a % 2
            print(b, end="")
            loops += 1
            if loops >= 20:
                return
