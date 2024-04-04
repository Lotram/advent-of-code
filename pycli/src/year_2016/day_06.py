from collections import Counter


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    counters = [Counter() for _ in range(len(lines[0]))]
    for line in lines:
        for idx, char in enumerate(line):
            counters[idx][char] += 1
    result = "".join(counter.most_common(1)[0][0] for counter in counters)
    return result


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    counters = [Counter() for _ in range(len(lines[0]))]
    for line in lines:
        for idx, char in enumerate(line):
            counters[idx][char] += 1
    result = "".join(counter.most_common(None)[-1][0] for counter in counters)
    return result
