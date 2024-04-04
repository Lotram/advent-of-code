vowels = set("aeiou")


def is_nice(chars):
    vowel_counter = 0
    current_char = None
    double_letters = False
    for char in chars:
        if char == current_char:
            double_letters = True
        if vowel_counter < 3 and char in vowels:
            vowel_counter += 1
        if f"{current_char}{char}" in {"ab", "cd", "pq", "xy"}:
            return False
        current_char = char
    return double_letters and (vowel_counter >= 3)


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    return sum(1 for line in lines if is_nice(line))


def is_nice_2(chars):
    pairs = set()
    rule_1 = False
    rule_2 = False
    for idx in range(2, len(chars)):
        if chars[idx] == chars[idx - 2]:
            rule_2 = True

        if (chars[idx - 1], chars[idx]) in pairs:
            rule_1 = True
        pairs.add((chars[idx - 2], chars[idx - 1]))

    return rule_1 and rule_2


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    return sum(1 for line in lines if is_nice_2(line))
