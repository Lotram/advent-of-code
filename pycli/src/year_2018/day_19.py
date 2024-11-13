from operator import methodcaller

from pydantic import BaseModel
from sympy import divisors

from .day_16 import registry


class Instruction(BaseModel):
    op: str
    values: tuple[int, int, int]
    counter: int = 0

    def apply(self, registers):
        self.counter += 1
        return registry[self.op](registers, *self.values)


class InstructionSet(BaseModel):
    ip_register: int
    instructions: list[Instruction]
    ip: int = 0
    counter: int = 0

    def run(self, registers):
        try:
            while 0 <= self.ip < len(self.instructions):
                # print(self.ip)
                registers[self.ip_register] = self.ip
                instruction = self.instructions[self.ip]
                registers = instruction.apply(registers)
                self.ip = registers[self.ip_register] + 1
                self.counter += 1

        except KeyboardInterrupt:
            pass
        print(f"finished after {self.counter} rounds")
        print(registers)
        for idx, instruction in enumerate(self.instructions):
            print(f"instruction #{idx} run {instruction.counter} times")
        return registers[0]


def parse(text):
    lines = text.strip().splitlines()
    ip_register = int(lines[0][-1])

    instructions = [
        Instruction(op=op, values=values)  # type: ignore
        for op, *values in map(methodcaller("split"), lines[1:])
    ]
    return InstructionSet(ip_register=ip_register, instructions=instructions)


def part_1(text, example: bool = False):
    instruction_set = parse(text)
    registers = {idx: 0 for idx in range(6)}
    result = instruction_set.run(registers)
    return result


def part_2(text, example: bool = False):
    # program returns the sum of divisors of the integer in registers[2]
    return sum(divisors(10551377))


"""
#0: addi 5 16 5 | f = 16 # jump to #16 to initialize

#1: seti 1 0 4 | e = 1
#2: seti 1 8 1 | b = 1 # end of init: {a: 0, b: 1, c: 10551377, d: 10550400, e: 1, f: 2}

#3: mulr 4 1 3 | d = e*b
#4: eqrr 3 2 3 | d = c == d # #3 -> #4 d = 1 if c == e * b else 0
#5: addr 3 5 5 | f = 5 + d # jump to #7 if c == e * b
#6: addi 5 1 5 | f = 7 # jump to #8
#7: addr 4 0 0 | a += e
#8: addi 1 1 1 | b += 1
#9: gtrr 1 2 3 | d = b > c
#10: addr 5 3 5 | f = d + 10 # jump to #12 if b > c else #3

#11: seti 2 4 5 | f = 2 # jump to #3



#12: addi 4 1 4 | e += 1 #13: gtrr 4 2 3 | d = e > c # finish program if e > c else back to #1
#14: addr 3 5 5 | f = 14 + d # jump to 16 if e > c
#15: seti 1 7 5 | f = 1
#16: mulr 5 5 5 | f = 16 * 16 # end of program

#17: addi 2 2 2 | c += 2
#18: mulr 2 2 2 | c *= c
#19: mulr 5 2 2 | c = 19 * c
#20: muli 2 11 2 | c *= 11 #17 -> #19: c = 209 * ((c + 2) ** 2). At start, c = 836

#21: addi 3 6 3 | d += 6
#22: mulr 3 5 3 | d *= 22
#23: addi 3 9 3 | d += 9 #21 -> #23: d = 22 * d + 141. At start, d = 141

#24: addr 2 3 2 | c += d #17 -> # 24: d = 22 * d +141, c =  209 * ((c + 2) ** 2) + 22 * d + 141. At start, c = 977

#25: addr 5 0 5 | f = 25 + a
#26: seti 0 5 5 | f = 0
#27: setr 5 9 3 | d = 27
#28: mulr 3 5 3 | d *= 28
#29: addr 5 3 3 | d += 29
#30: mulr 5 3 3 | d *= 30
#31: muli 3 14 3 | d *= 14
#32: mulr 3 5 3 | d *= 32 #27 -> #32: d = 10550400

#33: addr 2 3 2 | c += 10550400. At start, c = 10551377

#34: seti 0 1 0 | a = 0
#35: seti 0 0 5 | f = 0 # jump to #1
"""
