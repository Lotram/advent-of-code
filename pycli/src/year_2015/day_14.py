import re
from collections import Counter

pattern = re.compile(r"\d+")


TOTAL_DURATION = 2503


def solution(lines, total_duration):
    result = -1
    winners = set()
    for idx, line in enumerate(lines):
        speed, duration, rest = map(int, pattern.findall(line))
        distance = speed * (
            duration * (total_duration // (duration + rest))
            + min(duration, total_duration % (duration + rest))
        )
        if distance > result:
            winners = {idx}
            result = distance
        elif distance == result:
            winners.add(idx)

    return result, winners


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    return solution(lines, TOTAL_DURATION)[0]


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    scores = Counter()
    for idx in range(1, TOTAL_DURATION + 1):
        _, winners = solution(lines, idx)
        for winner in winners:
            scores[winner] += 1
    return scores.most_common(1)[0][1]
