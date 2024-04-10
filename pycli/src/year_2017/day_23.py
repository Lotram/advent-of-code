from collections import defaultdict

from sympy import divisors
from sympy.ntheory import isprime


def part_1(text, example: bool = False):
    registers = defaultdict(int)

    def value(x):
        return int(x) if x.lstrip("-").isdigit() else registers[x]

    instructions = list(text.strip().split("\n"))
    result = 0
    cursor = 0
    while 0 <= cursor < len(instructions):
        instruction = instructions[cursor]
        match instruction.split():
            case ["set", x, y]:
                registers[x] = value(y)
            case ["sub", x, y]:
                registers[x] -= value(y)
            case ["mul", x, y]:
                registers[x] *= value(y)
                result += 1

            case ["jnz", x, y]:
                if value(x) != 0:
                    cursor += int(y) - 1

            case _:
                raise ValueError(f"unknown command: {instruction}")

        cursor += 1
    return result


def part_2(text, example: bool = False):
    instructions = list(text.strip().split("\n"))

    def get_int_value(instruction_idx) -> int:
        return abs(int(instructions[instruction_idx].split()[-1]))

    step = get_int_value(-2)
    b = get_int_value(0) * get_int_value(4) + get_int_value(5)
    interval = get_int_value(7)
    assert step in divisors(interval)
    c = b + interval
    # the program loops on all integers between b and c (included) with a defined step
    # for each value which is not a prime, h is increased by one
    result = sum(1 for val in range(b, c + 1, step) if not isprime(val))
    return result
