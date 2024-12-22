from collections import defaultdict


MOD = 2**24


def next_secret(secret):
    secret ^= secret * 64
    secret %= MOD
    secret ^= secret // 32
    secret %= MOD
    secret ^= secret * 2048
    secret %= MOD
    return secret


def part_1(text, example: bool = False):
    numbers = list(map(int, text.strip().splitlines()))
    result = 0
    for number in numbers:
        value = number
        for _ in range(2000):
            value = next_secret(value)
        result += value

    return result


def part_2(text, example: bool = False):
    numbers = list(map(int, text.strip().splitlines()))
    result = 0
    price_per_sequence = defaultdict(int)
    for number in numbers:
        value = number
        differences = []
        seen_sequences = set()
        for idx in range(2000):
            new_value = next_secret(value)
            differences.append(new_value % 10 - value % 10)
            if idx >= 3 and (sequence := tuple(differences[-4:])) not in seen_sequences:
                price_per_sequence[sequence] += new_value % 10
                seen_sequences.add(sequence)
            value = new_value

    result = max(price_per_sequence.values())
    return result
