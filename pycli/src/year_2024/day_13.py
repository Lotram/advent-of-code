import re

from sympy import Matrix, linsolve, symbols


pattern = re.compile(r"\d+")
x, y = symbols("x,y", integer=True)


def parse_line(line):
    return map(int, pattern.findall(line))


def solve_machine(xa, ya, xb, yb, xp, yp, offset):
    equations = Matrix([[xa, xb], [ya, yb]])
    result = Matrix([xp + offset, yp + offset])
    x, y = symbols("x, y", integer=True, positive=True)
    results = list(linsolve((equations, result), x, y))  # pyright: ignore
    if len(results) == 0:
        return 0
    a, b = list(results)[0]

    if not (a.is_number and b.is_number):
        # happens if the rank of the matrix is 1. Apparently not the case here
        raise ValueError(a, b)

    if a.is_integer and b.is_integer:
        return 3 * a + b
    else:
        return 0


def part_1(text, example: bool = False):
    machines = text.strip().split("\n\n")
    result = 0
    for machine in machines:
        (xa, ya), (xb, yb), (xp, yp) = map(parse_line, machine.splitlines())
        result += solve_machine(xa, ya, xb, yb, xp, yp, offset=0)

    return result


def part_2(text, example: bool = False):
    machines = text.strip().split("\n\n")
    result = 0
    for machine in machines:
        (xa, ya), (xb, yb), (xp, yp) = map(parse_line, machine.splitlines())
        result += solve_machine(xa, ya, xb, yb, xp, yp, offset=10000000000000)

    return result
