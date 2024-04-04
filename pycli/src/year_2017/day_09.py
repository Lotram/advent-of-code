from itertools import count


def part_1(text, example: bool = False):
    cursor_it = count()
    group_depth = 0
    result = 0
    inside_garbage = False
    while (cursor := next(cursor_it)) < len(text):
        char = text[cursor]
        if inside_garbage:
            if char == ">":
                inside_garbage = False
            if char == "!":
                next(cursor_it)
        else:
            match char:
                case "{":
                    group_depth += 1
                    result += group_depth
                case "}":
                    group_depth -= 1
                case "<":
                    inside_garbage = True

    return result


def part_2(text, example: bool = False):
    cursor_it = count()
    result = 0
    inside_garbage = False
    while (cursor := next(cursor_it)) < len(text):
        char = text[cursor]
        if inside_garbage:
            if char == ">":
                inside_garbage = False
            elif char == "!":
                next(cursor_it)
            else:
                result += 1
        else:
            if char == "<":
                inside_garbage = True

    return result
