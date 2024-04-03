def results(size, values):
    match size, values:
        case 0, _:
            return 1
        case _, []:
            return 0
        case _:
            return results(size - values[-1], values[:-1]) + results(size, values[:-1])


def part_1(text, example: bool = False):
    size = 150
    values = list(map(int, text.strip().split("\n")))
    return results(size, values)


def results_2(size, values, used=0):
    match size, values:
        case 0, _:
            return 1, used
        case _, []:
            return 0, float("inf")
        case _:
            result_1, tot_used_1 = results_2(size - values[-1], values[:-1], used + 1)
            result_2, tot_used_2 = results_2(size, values[:-1], used)
            if tot_used_1 == tot_used_2:
                return result_1 + result_2, tot_used_1
            elif tot_used_1 < tot_used_2:
                return result_1, tot_used_1
            else:
                return result_2, tot_used_2


def part_2(text, example: bool = False):
    size = 150
    values = list(map(int, text.strip().split("\n")))
    return results_2(size, values)[0]
