import re
from collections import defaultdict, deque


pattern = re.compile(r"\d+")


def solution(player_count, marble_count):
    marbles = deque()
    score = defaultdict(int)
    for marble in range(marble_count):
        if marble and marble % 23 == 0:
            marbles.rotate(7)
            score[marble % player_count] += marble + marbles.popleft()
        else:
            marbles.rotate(-2)
            marbles.appendleft(marble)
    result = max(score.values())
    return result


def part_1(text, example: bool = False):
    player_count, marble_count = map(int, pattern.findall(text))
    return solution(player_count, marble_count)


def part_2(text, example: bool = False):
    player_count, marble_count = map(int, pattern.findall(text))
    return solution(player_count, marble_count * 100)
