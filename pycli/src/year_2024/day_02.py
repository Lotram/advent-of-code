def increasing(x, y):
    return x < y and y - x <= 3


def all_increasing(numbers):
    return all(increasing(*numbers[idx : idx + 2]) for idx in range(len(numbers) - 1))


def part_1(text, example: bool = False):
    result = 0
    for line in text.strip().splitlines():
        numbers = list(map(int, line.split()))
        result += int(all_increasing(numbers) or all_increasing(numbers[::-1]))
    return result


def part_2(text, example: bool = False):
    result = 0
    for line in text.strip().splitlines():
        numbers = list(map(int, line.split()))
        for idx in range(len(numbers)):
            _numbers = numbers.copy()
            _numbers.pop(idx)
            if all_increasing(_numbers) or all_increasing(_numbers[::-1]):
                result += 1
                break
    return result
