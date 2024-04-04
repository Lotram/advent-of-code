import re


def generator(seed, factor):
    previous = seed
    while True:
        value = (previous * factor) % 2147483647
        yield value & (2**16 - 1)
        previous = value


def part_1(text, example: bool = False):
    seed_a, seed_b = map(int, re.findall(r"\d+", text))
    gen_a = generator(seed_a, 16807)
    gen_b = generator(seed_b, 48271)
    result = sum(next(gen_a) == next(gen_b) for _ in range(40_000_000))

    return result


def generator_2(seed, factor, criteria):
    previous = seed
    while True:
        value = (previous * factor) % 2147483647
        if value % criteria == 0:
            yield value & (2**16 - 1)
        previous = value


def part_2(text, example: bool = False):
    seed_a, seed_b = map(int, re.findall(r"\d+", text))
    gen_a = generator_2(seed_a, 16807, 4)
    gen_b = generator_2(seed_b, 48271, 8)
    result = sum(next(gen_a) == next(gen_b) for _ in range(5_000_000))

    return result
