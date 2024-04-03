from collections import defaultdict
from operator import add, eq, ge, gt, le, lt, ne, sub

operators = {
    "<": lt,
    "<=": le,
    ">": gt,
    ">=": ge,
    "==": eq,
    "!=": ne,
    "inc": add,
    "dec": sub,
}


def part_1(text, example: bool = False):
    registers = defaultdict(int)
    for line in text.strip().split("\n"):
        register, op, value, _, cond_register, cond_op, cond_value = line.split()
        if not operators[cond_op](registers[cond_register], int(cond_value)):
            continue

        registers[register] = operators[op](registers[register], int(value))
    result = max(registers.values())
    return result


def part_2(text, example: bool = False):
    registers = defaultdict(int)
    result = 0
    for line in text.strip().split("\n"):
        register, op, value, _, cond_register, cond_op, cond_value = line.split()
        if not operators[cond_op](registers[cond_register], int(cond_value)):
            continue

        registers[register] = operators[op](registers[register], int(value))
        result = max(result, registers[register])
    return result
