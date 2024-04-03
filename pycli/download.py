from .utils import aoc, get_input_path, get_puzzle_path


def download(day: int, year: int):
    input_path = get_input_path(day, year)
    puzzle_path = get_puzzle_path(day, year)
    aoc(
        f"download -d {day} -y {year} --overwrite "
        f"--input-file {input_path} "
        f"--puzzle-file {puzzle_path}"
    )
    print("---")
    print(f'🎄 Successfully wrote input to "{input_path}".')
    print(f'🎄 Successfully wrote puzzle to "{puzzle_path}".')
