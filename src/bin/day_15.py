def _hash(text):
    current_value = 0
    for char in text:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256

    return current_value


def part_1(text):
    result = sum(_hash(data) for data in text.strip("\n").split(","))
    print(result)


def part_2(text):
    operations = text.strip("\n").split(",")
    boxes = [{} for _ in range(256)]
    for op in operations:
        label, op, length = op.partition("=") if "=" in op else op.partition("-")
        if op == "=":
            boxes[_hash(label)][label] = int(length)
        else:
            boxes[_hash(label)].pop(label, None)

    result = sum(
        box * slot * length
        for box, lenses in enumerate(boxes, 1)
        for slot, length in enumerate(lenses.values(), 1)
    )

    print(result)
