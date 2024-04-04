def part_1(text, example: bool = False):
    digits = list(text.strip())
    result = sum(
        int(digits[idx])
        for idx in range(len(digits))
        if digits[idx] == digits[(idx + 1) % len(digits)]
    )
    return result


def part_2(text, example: bool = False):
    digits = list(text.strip())
    result = sum(
        int(digits[idx])
        for idx in range(len(digits))
        if digits[idx] == digits[(idx + (len(digits) // 2)) % len(digits)]
    )
    return result
