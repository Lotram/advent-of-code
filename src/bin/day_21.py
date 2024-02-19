def swap(password, x, y):
    password[x], password[y] = password[y], password[x]
    return password


def rotate(password, shift, reverse=False):
    if reverse:
        shift = -shift
    shift %= len(password)
    return password[-shift:] + password[:-shift]


INDEX_ROTATIONS = [(2 * i + 1 + (i >= 4)) % 8 for i in range(8)]


def rotate_index(password, X, reverse=False):
    x_idx = password.index(X)
    if reverse:
        previous_idx = INDEX_ROTATIONS.index(x_idx)
    else:
        previous_idx = INDEX_ROTATIONS[password.index(X)]
    return rotate(password, (previous_idx - x_idx) % len(password))


def reverse(password, x, y):
    return password[:x] + password[y : x - 1 if x else None : -1] + password[y + 1 :]


def move(password, x, y, reverse=False):
    if reverse:
        x, y = y, x

    password.insert(y, password.pop(x))
    return password


def part_1(text):
    password = list("abcdefgh")

    for operation in text.strip().split("\n"):
        match operation.split():
            case ["swap", "position", X, "with", "position", Y]:
                password = swap(password, int(X), int(Y))
            case ["swap", "letter", X, "with", "letter", Y]:
                password = swap(password, password.index(X), password.index(Y))
            case ["rotate", direction, X, _]:
                shift = int(X) if direction == "right" else -int(X)
                password = rotate(password, shift)
            case ["rotate", "based", *_, X]:
                password = rotate_index(password, X)
            case ["reverse", "positions", X, "through", Y]:
                password = reverse(password, int(X), int(Y))
            case ["move", "position", X, *_, Y]:
                password = move(password, int(X), int(Y))
            case _:
                raise ValueError(operation)

    result = "".join(password)
    return result


def part_2(text):
    password = list("fbgdceah")
    for operation in text.strip().split("\n")[::-1]:
        match operation.split():
            case ["swap", "position", X, "with", "position", Y]:
                password = swap(password, int(X), int(Y))

            case ["swap", "letter", X, "with", "letter", Y]:
                password = swap(password, password.index(X), password.index(Y))

            case ["rotate", direction, X, _]:
                shift = int(X) if direction == "right" else -int(X)
                password = rotate(password, shift, reverse=True)
            case ["rotate", "based", *_, X]:
                password = rotate_index(password, X, reverse=True)
            case ["reverse", "positions", X, "through", Y]:
                password = reverse(password, int(X), int(Y))
            case ["move", "position", X, *_, Y]:
                password = move(password, int(X), int(Y), reverse=True)
            case _:
                raise ValueError(operation)

    result = "".join(password)
    return result
