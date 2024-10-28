import re
from typing import NamedTuple


registry = {}


pattern = re.compile(r"\d+")


def from_string(data):
    return map(int, pattern.findall(data))


class Sample(NamedTuple):
    before: dict[int, int]
    op_code: int
    args: tuple[int, int, int]
    after: dict[int, int]

    def check_op(self, op):
        return op(self.before, *self.args) == self.after

    def valid_ops(self, ops):
        return {name: op for name in ops if self.check_op(op := registry[name])}

    @classmethod
    def parse(cls, sample_data):
        _before, _args, _after = sample_data.split("\n")
        before = dict(enumerate(from_string(_before)))
        op_code, *args = from_string(_args)
        after = dict(enumerate(from_string(_after)))

        args = tuple(args)
        assert len(args) == 3

        return cls(before, op_code, args, after)


def op(func):
    registry[func.__name__] = func
    return func


@op
def addr(registers, a, b, c):
    return registers | {c: registers[a] + registers[b]}


@op
def addi(registers, a, b, c):
    return registers | {c: registers[a] + b}


@op
def mulr(registers, a, b, c):
    return registers | {c: registers[a] * registers[b]}


@op
def muli(registers, a, b, c):
    return registers | {c: registers[a] * b}


@op
def banr(registers, a, b, c):
    return registers | {c: registers[a] & registers[b]}


@op
def bani(registers, a, b, c):
    return registers | {c: registers[a] & b}


@op
def borr(registers, a, b, c):
    return registers | {c: registers[a] | registers[b]}


@op
def bori(registers, a, b, c):
    return registers | {c: registers[a] | b}


@op
def setr(registers, a, b, c):
    return registers | {c: registers[a]}


@op
def seti(registers, a, b, c):
    return registers | {c: a}


@op
def gtir(registers, a, b, c):
    return registers | {c: int(a > registers[b])}


@op
def gtri(registers, a, b, c):
    return registers | {c: int(registers[a] > b)}


@op
def gtrr(registers, a, b, c):
    return registers | {c: int(registers[a] > registers[b])}


@op
def eqir(registers, a, b, c):
    return registers | {c: int(a == registers[b])}


@op
def eqri(registers, a, b, c):
    return registers | {c: int(registers[a] == b)}


@op
def eqrr(registers, a, b, c):
    return registers | {c: int(registers[a] == registers[b])}


def parse(text):
    _samples, test_program = text.split("\n\n\n\n")
    samples = list(map(Sample.parse, _samples.split("\n\n")))

    return samples, test_program


def part_1(text, example: bool = False):
    samples, _ = parse(text)

    result = sum(1 for sample in samples if len(sample.valid_ops(registry)) >= 3)
    return result


def part_2(text, example: bool = False):
    samples, test_program = parse(text)
    ops = {idx: None for idx in range(16)}
    missing_ops = set(registry)
    while any(op is None for op in ops.values()):
        for sample in samples:
            if len(valid_ops := sample.valid_ops(missing_ops)) == 1:
                name = set(valid_ops).pop()
                ops[sample.op_code] = registry[name]
                missing_ops.remove(name)

    registers = {idx: 0 for idx in range(4)}
    for op_code, *args in map(from_string, test_program.splitlines()):
        registers = ops[op_code](registers, *args)

    result = registers[0]
    return result
