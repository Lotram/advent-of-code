from operator import and_, invert, lshift, or_, rshift

from pydantic import BaseModel

SIZE = 2**16 - 1

OPERATORS = {"NOT": invert, "LSHIFT": lshift, "RSHIFT": rshift, "AND": and_, "OR": or_}


class State(BaseModel):
    wires: dict[str, int | str]

    def parse(self, inputs) -> int:
        match inputs.split():
            case [value]:
                return self.get(value)
            case [op, value]:
                assert op == "NOT"
                values = [self.get(value)]
            case [val1, op, val2]:
                values = [self.get(val1), self.get(val2)]
        return OPERATORS[op](*values)

    def get(self, wire) -> int:
        if wire.isdigit():
            return int(wire)
        value = self.wires[wire]
        if isinstance(value, str):
            self.wires[wire] = self.parse(value)

        return self.wires[wire]


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    wires = {}
    for line in lines:
        inputs, output = line.split(" -> ")
        wires[output] = inputs.strip()
    state = State(wires=wires)
    result = state.get("a") & SIZE
    return result


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    wires = {}
    for line in lines:
        inputs, output = line.split(" -> ")
        wires[output] = inputs.strip()
    _wires = wires.copy()
    state = State(wires=wires)
    result = state.get("a") & SIZE
    new_state = State(wires=_wires)
    new_state.wires["b"] = str(result)
    result = new_state.get("a") & SIZE
    return result
