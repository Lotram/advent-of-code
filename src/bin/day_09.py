import re
from collections import deque
from itertools import takewhile

from pydantic import BaseModel


class Token(BaseModel):
    start: int
    end: int
    count: int = 1


class Char(Token):
    pass


class Marker(Token):
    char_count: int
    multiplier: int


def part_1(text):
    text = text.strip()
    pattern = re.compile(r"\((?P<char_count>\d+)x(?P<multiplier>\d+)\)")
    cursor = -1
    result = len(text)
    skipped = []
    for match_ in pattern.finditer(text):
        if match_.start() <= cursor:
            skipped.append(match_.group())
            continue
        char_count, multiplier = map(int, match_.groups())
        result += char_count * (multiplier - 1) - len(match_.group())
        cursor = match_.end() + char_count - 1
    return result


def part_2(text):
    text = text.strip()
    pattern = re.compile(r"\((?P<char_count>\d+)x(?P<multiplier>\d+)\)")
    tokens = deque()
    for match_ in pattern.finditer(text):
        char_count, multiplier = map(int, match_.groups())
        for char in range(tokens[-1].end if tokens else 0, match_.start()):
            tokens.append(Char(start=char, end=char + 1))
        tokens.append(
            Marker(
                start=match_.start(),
                end=match_.end(),
                char_count=char_count,
                multiplier=multiplier,
            )
        )

    for char in range(tokens[-1].end, len(text)):
        tokens.append(Char(start=char, end=char + 1))

    result = 0
    while tokens:
        token = tokens.popleft()
        if isinstance(token, Marker):
            for tok in takewhile(
                lambda tok: tok.start < token.end + token.char_count, tokens
            ):
                # this works because, looking at the input,
                # if a marker multiplies another marker, it also
                # multiplies all chars decompressed by this other marker
                tok.count *= token.multiplier
        else:
            result += token.count

    return result
