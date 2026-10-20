from collections import defaultdict


def part_1(text, example: bool = False):
    lines = text.splitlines()
    beams = {lines[0].index("S")}
    result = 0
    for line in lines[2::2]:
        splitters = {idx for idx, char in enumerate(line) if char == "^"}
        matching_splitters = beams & splitters
        result += len(matching_splitters)
        new_beams = {elem + diff for elem in matching_splitters for diff in (-1, 1)}
        beams = new_beams | (beams - splitters)

    return result


def part_2(text, example: bool = False):
    lines = text.splitlines()
    beams = defaultdict(int, {lines[0].index("S"): 1})
    for line in lines[2::2]:
        splitters = {idx for idx, char in enumerate(line) if char == "^"}
        matching_splitters = beams.keys() & splitters
        for elem in matching_splitters:
            split_count = beams.pop(elem)
            beams[elem + 1] += split_count
            beams[elem - 1] += split_count

    result = sum(beams.values())
    return result
