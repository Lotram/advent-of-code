import re

from pydantic import BaseModel


class Computer(BaseModel):
    instructions: list[int]
    registers: list[int] = [0, 0, 0]
    pointer: int = 0
    outputs: list[int] = []

    def get_combo(self, value):
        if 0 <= value <= 3:
            return value
        if 4 <= value <= 6:
            return self.registers[value - 4]

        raise ValueError(f"wrong combo {value}")

    def adv(self, operand):
        return self.registers[0] // (2 ** self.get_combo(operand))

    def output(self, value):
        self.outputs.append(value)

    def run(self):
        while True:
            opcode, operand = self.instructions[self.pointer : self.pointer + 2]
            match opcode:
                case 0:  # adv
                    self.registers[0] = self.adv(operand)
                case 1:  # bxl
                    self.registers[1] ^= operand
                case 2:  # bst
                    self.registers[1] = self.get_combo(operand) % 8
                case 3:  # jnz
                    if self.registers[0] != 0:
                        self.pointer = operand
                        continue  # avoid modifying the pointer once more
                case 4:  # bxc
                    self.registers[1] ^= self.registers[2]
                case 5:  # out
                    self.output(self.get_combo(operand) % 8)

                case 6:  # bdv
                    self.registers[1] = self.adv(operand)
                case 7:  # cdv
                    self.registers[2] = self.adv(operand)

            self.pointer += 2
            if not 0 <= self.pointer < len(self.instructions):
                break

    def reset(self):
        self.pointer = 0
        self.outputs = []


def parse(text):
    return map(int, re.findall(r"\d+", text))


def part_1(text, example: bool = False):
    a, b, c, *instructions = parse(text)
    computer = Computer(registers=[a, b, c], instructions=instructions)
    computer.run()
    result = ",".join(map(str, computer.outputs))
    return result


def h(a):
    return ((a % 8) ^ 7 ^ (a >> ((a % 8) ^ 1))) % 8


def part_2(text, example: bool = False):
    """
    def programm(a):
        outputs = []
        while a > 0:
            outputs.append(h(a))
            a //= 3

        return outputs

    """
    a, b, c, *instructions = parse(text)

    candidates = [0]
    for value in reversed(instructions):
        candidates = [
            x * 8 + i for x in candidates for i in range(8) if h(x * 8 + i) == value
        ]

    return min(candidates)
