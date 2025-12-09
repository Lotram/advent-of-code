def part_1(text, example: bool = False):
    value = 50
    result = 0
    for line in text.splitlines():
        sign = 1 if line[0] == "R" else -1
        value += sign * int(line[1:])
        value %= 100
        if value == 0:
            result += 1

    return result


# def part_2(text, example: bool = False):
#     value = 50
#     result = 0
#     for line in text.splitlines():
#         sign = 1 if line[0] == "R" else -1
#         rotations = int(line[1:])

#         if line[0] == "R":
#             result += int((value + rotations) // 100)
#         else:
#             result += int(abs((value - rotations - 0.5) // 100)) - (value == 0)

#         value = (value + sign * rotations) % 100

#     return result


def part_2(text, example: bool = False):
    value = 50
    result = 0
    for line in text.splitlines():
        sign = 1 if line[0] == "R" else -1
        rotations = int(line[1:])

        for _ in range(rotations):
            value += sign
            value %= 100
            if value == 0:
                result += 1

    return result
