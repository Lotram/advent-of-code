from functools import partial, reduce
from itertools import batched
from operator import xor


def knot_hash_round(size, lengths, rounds=1):
    values = list(range(size))
    skip = 0
    current_position = 0
    for _ in range(rounds):
        for length in lengths:
            if length > size:
                raise ValueError(f"length {length} > size {size}")

            for idx in range(length // 2):
                idx_a = (current_position + idx) % size
                idx_b = (current_position + length - idx - 1) % size
                values[idx_a], values[idx_b] = values[idx_b], values[idx_a]

            current_position += skip + length
            current_position %= size
            skip += 1
    return values


def knot_hash(text):
    size = 256
    lengths = [*map(int, map(ord, text.strip())), 17, 31, 73, 47, 23]
    values = knot_hash_round(size, lengths, rounds=64)
    dense = map(partial(reduce, xor), batched(values, 16))

    return "".join(f"{value:0>2x}" for value in dense)


def part_1(text):
    size = 256
    lengths = map(int, text.split(","))
    values = knot_hash_round(size, lengths)
    result = values[0] * values[1]
    return result


def part_2(text):
    result = knot_hash(text)
    return result
