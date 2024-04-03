def redistribute(blocks):
    value = max(blocks)
    size = len(blocks)
    idx = blocks.index(max(blocks))
    blocks[idx] = 0
    return tuple(
        blocks[i] + value // size + ((i - idx - 1) % size < value % size)
        for i in range(size)
    )


def part_1(text):
    seen = set()
    blocks = tuple(map(int, text.strip().split()))
    result = 0
    while blocks not in seen:
        seen.add(blocks)
        blocks = redistribute(list(blocks))
        result += 1

    return result


def part_2(text):
    seen = {}
    blocks = tuple(map(int, text.strip().split()))
    loops = 0
    while blocks not in seen:
        seen[blocks] = loops
        blocks = redistribute(list(blocks))
        loops += 1

    result = loops - seen[blocks]
    return result
