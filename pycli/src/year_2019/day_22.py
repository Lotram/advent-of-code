from functools import cache, partial


def new_stack(val, size):
    return size - val - 1


def cut(val, n, size):
    return (val - n) % size


def incremental(val, n, size):
    return (val * n) % size


@cache
def modular_inverse(n, size):
    return pow(n, -1, size)


def get_operations(text, size, reverse=False):

    _new_stack = partial(new_stack, size=size)
    _cut = partial(cut, size=size)
    _incremental = partial(incremental, size=size)
    operations = []
    for line in text.splitlines():
        match line.split():
            case ["cut", value]:
                n = int(value)
                op = partial(_cut, n=size - n if reverse else n)
            case ["deal", "into", *_]:
                op = _new_stack
            case ["deal", "with", "increment", value]:
                n = int(value)
                op = partial(_incremental, n=modular_inverse(n, size) if reverse else n)
            case _:
                print(line)
                raise ValueError(line)

        operations.append(op)

    if reverse:
        return list(reversed(operations))
    return operations


def part_1(text, example: bool = False):
    operations = get_operations(text, 10007)
    value = 2019
    for op in operations:
        value = op(value)
    return value


def run(value, ops):
    for op in ops:
        value = op(value)
    return value


def part_2(text, example: bool = False):
    L = 119315717514047
    n = 101741582076661
    inv_ops = get_operations(text, L, reverse=True)

    # all operations are linear, meaning run is linear on value,
    # i.e it can be written y = a * x + b (in Z/LZ ring)
    # we then get
    x = 2020
    y = run(x, inv_ops)
    z = run(y, inv_ops)
    a = ((z - y) * modular_inverse(y - x, L)) % L
    b = (y - a * x) % L

    # if f(x) = ax + b, then f^n(x) = a^n*x + b * (a^n - 1) / (a - 1)
    return (pow(a, n, L) * x + b * (pow(a, n, L) - 1) * modular_inverse(a - 1, L)) % L
