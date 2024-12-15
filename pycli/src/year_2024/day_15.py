from pycli.src.grid import EAST, NORTH, SOUTH, WEST, Grid


DIRECTIONS = {"<": WEST, "^": NORTH, ">": EAST, "v": SOUTH}


def move(grid, instruction, position):
    direction = DIRECTIONS[instruction]
    match grid[(next_position := position + direction)]:
        case "#":
            return position

        case ".":
            pass

        case "O":
            _position = next_position
            while grid[_position] == "O":
                _position += direction

            if grid[_position] == "#":
                return position

            if grid[_position] == ".":
                grid[_position] = "O"

    grid[position] = "."
    position = next_position
    return position


def run(grid, instructions):
    position = grid.find("@")
    grid.replace("@", ".")
    for instruction in instructions.replace("\n", "").strip():
        position = move(grid, instruction, position)


def part_1(text, example: bool = False):
    grid_text, instructions = text.strip().split("\n\n")
    grid = Grid.from_text(grid_text)
    run(grid, instructions)
    result = sum(100 * box.row + box.col for box in grid.find_all("O"))

    return result


def can_move_box_horizontally(grid, position, direction, next_positions):
    _position = position + direction
    next_positions[_position] = "."
    while grid[_position] in {"[", "]"}:
        next_positions[_position + direction] = grid[_position]
        _position += direction

    if grid[_position] == "#":
        return False

    if grid[_position] == ".":
        return True


def can_move_box_vertically(grid, position, direction, next_positions):
    if grid[position + direction] == ".":
        return True
    if grid[position + direction] == "#":
        print("should not pass here")
        return False

    if grid[position + direction] == "[":
        box_position = (position + direction, position + direction + EAST)
    else:
        box_position = (position + direction + WEST, position + direction)

    if any(grid[_position + direction] == "#" for _position in box_position):
        return False

    next_positions.update(
        {_position + direction: char for char, _position in zip("[]", box_position)}
    )
    for _position in box_position:
        next_positions.setdefault(_position, ".")

    if all(grid[_position + direction] == "." for _position in box_position):
        return True

    return all(
        can_move_box_vertically(grid, _position, direction, next_positions)
        for _position in box_position
    )


def can_move_box(grid, position, direction, next_positions):
    if direction in {EAST, WEST}:
        return can_move_box_horizontally(grid, position, direction, next_positions)

    return can_move_box_vertically(grid, position, direction, next_positions)


def move_2(grid, instruction, position, step):
    direction = DIRECTIONS[instruction]
    match grid[(next_position := position + direction)]:
        case "#":
            return position

        case ".":
            pass

        case "[" | "]":
            next_positions = {}
            if can_move_box(grid, position, direction, next_positions):
                for _pos, char in next_positions.items():
                    grid[_pos] = char

            else:
                return position

    position = next_position
    return position


def run_2(grid, instructions):
    position = grid.find("@")

    grid.replace("@", ".")
    for step, instruction in enumerate(instructions.replace("\n", "").strip()):
        position = move_2(grid, instruction, position, step)


def part_2(text, example: bool = False):
    grid_text, instructions = text.strip().split("\n\n")
    grid_text = (
        grid_text.replace(".", "..")
        .replace("#", "##")
        .replace("O", "[]")
        .replace("@", "@.")
    )
    grid = Grid.from_text(grid_text)
    run_2(grid, instructions)
    result = sum(100 * box.row + box.col for box in grid.find_all("["))

    return result
