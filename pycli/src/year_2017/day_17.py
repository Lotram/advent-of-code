def part_1(text, example: bool = False):
    steps = int(text.strip())
    buffer = [0]
    current_position = 0
    for idx in range(1, 2018):
        current_position = (current_position + steps) % idx + 1
        buffer.insert(current_position, idx)
    result = buffer[(buffer.index(2017) + 1) % len(buffer)]
    return result


def part_2(text, example: bool = False):
    steps = int(text.strip())
    current_position = 0
    for idx in range(1, 5_000_001):
        current_position = (current_position + steps) % idx + 1
        if current_position == 1:
            result = idx
    return result
