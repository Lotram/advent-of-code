import re

from .utils import aoc, get_answer_path, get_input_path, get_puzzle_path


answer_pattern = re.compile(r"Your puzzle answer was `(?P<answer>[a-zA-Z0-9_,]+)`.")


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

    puzzle_content = puzzle_path.read_text()
    answers = answer_pattern.findall(puzzle_content)
    if answers:
        get_answer_path(day, year).write_text("\n".join(answers))
        print("🎄 Successfully wrote answers.")
