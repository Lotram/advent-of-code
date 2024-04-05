import re


def solve(text, numbers):
    lines = text.strip().split("\n")

    reversed_numbers = {key[::-1]: value for key, value in numbers.items()}

    pattern = re.compile(r"|".join(numbers))
    reversed_pattern = re.compile(
        r"|".join("".join(reversed(number)) for number in numbers)
    )

    total = 0

    for line in lines:
        first_digit = numbers[pattern.search(line).group(0)]
        last_digit = reversed_numbers[reversed_pattern.search(line[::-1]).group(0)]
        total += int(f"{first_digit}{last_digit}")

    return total


digits = {str(i): str(i) for i in range(1, 10)}

numbers = {
    **digits,
    "zero": str(0),
    "one": str(1),
    "two": str(2),
    "three": str(3),
    "four": str(4),
    "five": str(5),
    "six": str(6),
    "seven": str(7),
    "eight": str(8),
    "nine": str(9),
}


def part_1(text, example=False):
    return solve(text, digits)


def part_2(text, example=False):
    return solve(text, numbers)
