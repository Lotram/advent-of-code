from functools import cache


def part_1(text):
    lines = text.strip().split("\n")
    start = next(
        (row, col)
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
        if char == "S"
    )

    @cache
    def get_neigbhours(tile):
        neighbours = set()
        for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            row = tile[0] + dir[0]
            col = tile[1] + dir[1]
            if (
                0 <= row < len(lines)
                and 0 <= col < len(lines[0])
                and lines[row][col] != "#"
            ):
                neighbours.add((row, col))
        return neighbours

    def get_tiles(n):
        if n == 0:
            return {start}
        n_1 = get_tiles(n - 1)
        result = set()
        for tile in n_1:
            result |= get_neigbhours(tile)
        return result

    result = len(get_tiles(10))
    return result


def part_2(text):
    lines = text.strip().split("\n")
    size = len(lines)
    assert len(lines[0]) == size
    half_size = int((size - 1) / 2)
    chars = {
        (row - half_size, col - half_size): char
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
    }

    for (row, col), char in chars.items():
        if char == "#" or abs(row) == half_size or abs(col) == half_size:
            continue

        if (
            f"{chars[row + 1, col]}{chars[row - 1, col]}{chars[row, col - 1]}{chars[row, col + 1]}"
            == "####"
        ):
            chars[row, col] = "#"

    inside_odd_count = sum(
        1
        for (row, col), char in chars.items()
        if char == "#" and (row + col) % 2 == 1 and abs(row) + abs(col) <= half_size
    )
    inside_even_count = sum(
        1
        for (row, col), char in chars.items()
        if char == "#" and (row + col) % 2 == 0 and abs(row) + abs(col) <= half_size
    )
    outside_count = sum(
        1
        for (row, col), char in chars.items()
        if char == "#" and abs(row) + abs(col) > half_size
    )

    loops = 26501365

    k = loops // size
    assert loops == k * size + half_size

    result = (
        (loops + 1) ** 2
        - k**2 * inside_even_count
        - (k + 1) ** 2 * inside_odd_count
        - k * (k + 1) * outside_count
    )
    return result
