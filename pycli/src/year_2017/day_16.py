def dance(moves, programs):
    for move in moves:
        match move[0]:
            case "s":
                x = int(move[1:])
                programs = [*programs[-x:], *programs[:-x]]
            case "x":
                a, b = map(int, move[1:].split("/"))
                programs[a], programs[b] = programs[b], programs[a]
            case "p":
                a, b = move[1:].split("/")
                idx_a = programs.index(a)
                idx_b = programs.index(b)
                programs[idx_a], programs[idx_b] = programs[idx_b], programs[idx_a]
    return programs


def part_1(text, example: bool = False):
    programs = [chr(idx) for idx in range(ord("a"), ord("p") + 1)]
    programs = dance(text.strip().split(","), programs)
    result = "".join(programs)
    return result


def part_2(text, example: bool = False):
    programs = [chr(idx) for idx in range(ord("a"), ord("p") + 1)]
    seen = {}
    counter = 0
    while True:
        programs = dance(text.strip().split(","), programs)
        value = "".join(programs)
        if value in seen:
            break
        seen[value] = counter
        counter += 1

    loop_start = seen[value]
    loop_size = counter - loop_start
    print(loop_start, loop_size)
    result = list(seen)[(10**9 - 1 - loop_start) % loop_size]

    return result
