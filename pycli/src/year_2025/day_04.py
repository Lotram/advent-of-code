from pycli.src.grid import Grid


def part_1(text, example: bool = False):
    grid = Grid.from_text(text, diag=True)

    result = sum(
        1
        for position in grid.find_iter("@")
        if sum(val == "@" for _, val in grid.neighbours(position)) < 4
    )
    return result


def part_2(text, example: bool = False):
    grid = Grid.from_text(text, diag=True)
    result = 0
    # with Live(grid) as live:
    while True:
        positions = []
        for position in grid.find_iter("@"):
            if sum(val == "@" for _, val in grid.neighbours(position)) < 4:
                positions.append(position)

        if not positions:
            break

        result += len(positions)
        for position in positions:
            grid[position] = "."

            # live.update(grid)

    return result
