from functools import reduce
from itertools import combinations, count
from operator import xor

import numpy as np
from pydantic import BaseModel
from scipy.optimize import LinearConstraint, milp


class Machine(BaseModel):
    lights: int
    buttons: list[int]
    joltages: list[int]

    @classmethod
    def parse_line(cls, line):
        _lights, *_buttons, _joltages = line.split()
        lights = sum((char == "#") * 2**i for i, char in enumerate(_lights[1:-1]))
        buttons = [tuple(map(int, button[1:-1].split(","))) for button in _buttons]
        joltages = list(map(int, _joltages[1:-1].split(",")))
        return cls(
            lights=lights,
            buttons=[sum(2 ** int(i) for i in button) for button in buttons],
            joltages=joltages,
        )


def part_1(text, example: bool = False):

    machines = list(map(Machine.parse_line, text.splitlines()))
    result = 0
    for machine in machines:
        for k in count(1):
            if any(
                reduce(xor, combination) == machine.lights
                for combination in combinations(machine.buttons, k)
            ):
                result += k
                break
    return result


def part_2(text, example: bool = False):
    machines = list(map(Machine.parse_line, text.splitlines()))
    result = 0
    for machine in machines:
        A_T = np.array(
            [
                [int(char) for char in reversed(f"{value:0{len(machine.joltages)}b}")]
                for value in machine.buttons
            ]
        ).transpose()
        b = np.array(machine.joltages)
        solution = milp(
            c=np.ones(len(machine.buttons)),  # minimize sum(x)
            integrality=np.ones(len(machine.buttons)),  # every variable is integer
            constraints=LinearConstraint(A_T, b, b),
        )
        assert solution.success, solution
        result += int(solution.fun)
    return result
