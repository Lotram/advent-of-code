def _parse(group):
    for idx in range(3, len(group)):
        if (
            group[idx] == group[idx - 3]
            and group[idx - 1] == group[idx - 2]
            and group[idx] != group[idx - 1]
        ):
            return True
    return False


def parse(line):
    inside = False
    has_abba = False
    for group in line.replace("]", "[").split("["):
        if _parse(group):
            if inside:
                return False
            else:
                has_abba = True
        inside = not inside

    return has_abba


def part_1(text):
    lines = text.strip().split("\n")
    result = sum(1 for line in lines if parse(line))
    return result


def _parse_2(group, inside):
    abas = set()
    for idx in range(2, len(group)):
        if group[idx] == group[idx - 2] and group[idx] != group[idx - 1]:
            abas.add((group[idx - (1 - inside)], group[idx - inside]))
    return abas


def parse_2(line):
    inside = False
    inside_abas = set()
    outside_abas = set()
    for group in line.replace("]", "[").split("["):
        _abas = _parse_2(group, inside)
        if inside:
            inside_abas.update(_abas)
        else:
            outside_abas.update(_abas)
        inside = not inside

    return bool(inside_abas & outside_abas)


def part_2(text):
    lines = text.strip().split("\n")
    result = sum(1 for line in lines if parse_2(line))
    return result
