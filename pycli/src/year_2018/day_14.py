from collections import deque


def part_1(text, example: bool = False):
    length = int(text.strip())
    recipes = ["3", "7"]
    c0, c1 = 0, 1
    while len(recipes) < length + 10:
        r0, r1 = recipes[c0], recipes[c1]
        for char in str(int(r0) + int(r1)):
            recipes.append(char)

        c0 = (c0 + 1 + int(r0)) % len(recipes)
        c1 = (c1 + 1 + int(r1)) % len(recipes)

    result = "".join(map(str, recipes[-10:]))
    return result


def part_2(text, example: bool = False):
    substring = deque(text.strip())
    recipes = ["3", "7"]
    c0, c1 = 0, 1
    last_chars = deque()
    while True:
        r0, r1 = recipes[c0], recipes[c1]
        for char in str(int(r0) + int(r1)):
            recipes.append(char)
            if len(last_chars) >= len(substring):
                last_chars.popleft()
            last_chars.append(char)
            if last_chars == substring:
                return len(recipes) - len(substring)

        c0 = (c0 + 1 + int(r0)) % len(recipes)
        c1 = (c1 + 1 + int(r1)) % len(recipes)
