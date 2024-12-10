from collections import deque
from itertools import chain, starmap, takewhile
from operator import mul


def part_1(text, example: bool = False):
    blocks = deque(map(int, text.strip()))
    disk = list(
        chain.from_iterable(
            [None] * block if idx % 2 else [idx // 2] * block
            for idx, block in enumerate(map(int, blocks))
        )
    )
    back_cursor = len(disk) - 1
    cursor = disk.index(None)
    while cursor < back_cursor:
        match disk[cursor], disk[back_cursor]:
            case (None, int()):
                disk[cursor] = disk[back_cursor]
                disk[back_cursor] = None
                back_cursor -= 1
            case (None, None):
                back_cursor -= 1
            case (int(), _):
                cursor += 1
    result = sum(starmap(mul, enumerate(takewhile(lambda e: e is not None, disk))))
    return result


def part_2(text, example: bool = False):
    blocks = deque(map(int, text.strip()))

    files = []
    available_memory = []
    cursor = 0
    for idx, size in enumerate(blocks):
        if idx % 2 and size:
            available_memory.append((cursor, size))
        else:
            files.append((cursor, size, idx // 2))
        cursor += size

    result = 0

    for file_position, file_size, block_id in files[::-1]:
        try:
            (idx, (position, size)) = next(
                item
                for item in enumerate(
                    takewhile(
                        lambda item, file_position=file_position: item[0]
                        < file_position,
                        available_memory,
                    )
                )
                if file_size <= item[1][1]
            )
            if size == file_size:
                available_memory.pop(idx)
            else:
                available_memory[idx] = (position + file_size, size - file_size)
            new_position = position

        except:
            new_position = file_position

        result += block_id * sum(range(new_position, new_position + file_size))

    return result
