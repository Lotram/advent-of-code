import re


def part_1(lines):
    print(lines.split("\n")[:3])


def part_2(lines):
    numbers = {
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
        **{str(i): str(i) for i in range(1, 10)},
    }

    reversed_numbers = {key[::-1]: value for key, value in numbers.items()}

    def replace(matchobj):
        return numbers[matchobj.group(0)]

    pattern = re.compile(r"|".join(numbers))
    reversed_pattern = re.compile(
        r"|".join("".join(reversed(number)) for number in numbers)
    )

    total = 0

    calibrations = []

    for line in lines.strip().split("\n"):
        first_digit = numbers[pattern.search(line).group(0)]
        last_digit = reversed_numbers[reversed_pattern.search(line[::-1]).group(0)]
        number = int(f"{first_digit}{last_digit}")
        calibrations.append(number)

    print("calibrations", sum(calibrations))

    total = 0

    for i, line in enumerate(lines.strip().split("\n")):
        digits = [char for char in pattern.sub(replace, line) if char.isdigit()]
        number = int(f"{digits[0]}{digits[-1]}")

        total += number

    print("total:", total)
