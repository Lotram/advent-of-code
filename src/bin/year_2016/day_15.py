import re

from sympy.ntheory.modular import solve_congruence


def parse_text(text):
    equations = []
    pattern = re.compile(r"\d+")
    for line in text.strip().split("\n"):
        idx, modulo, _, start_position = map(int, pattern.findall(line))
        equations.append((-idx - start_position, modulo))
    return equations


def part_1(text):
    equations = parse_text(text)
    result = solve_congruence(*equations)[0]
    return result


def part_2(text):
    equations = parse_text(text)
    equations.append((-len(equations) - 1, 11))
    result = solve_congruence(*equations)[0]
    return result
