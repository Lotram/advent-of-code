import re
from collections import Counter
from operator import itemgetter

pattern = re.compile(r"(?P<name>[a-z-]+)-(?P<room_id>\d+)\[(?P<checksum>[a-z]{5})\]")


def key(tup):
    letter, counter = tup
    return -counter, letter


def rotate_char(char, value):
    if char == "-":
        return char
    return chr((ord(char) - ord("a") + value) % 26 + ord("a"))


def rotate(name, value):
    # value = value % 26
    return "".join(rotate_char(char, value) for char in name).replace("-", " ")


def get_real_rooms(lines):
    for line in lines:
        name, room_id, checksum = pattern.match(line).groups()
        most_common = sorted(Counter(name.replace("-", "")).most_common(None), key=key)
        if "".join(map(itemgetter(0), most_common[:5])) == checksum:
            yield (name, int(room_id))


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    result = sum(room_id for _, room_id in get_real_rooms(lines))

    return result


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    for name, room_id in get_real_rooms(lines):
        decrypted = rotate(name, room_id)
        if decrypted == "northpole object storage":
            return room_id
    result = None
    return result
