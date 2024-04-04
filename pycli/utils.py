import subprocess
from pathlib import Path
from typing import Literal


def data_path(
    day: int, year: int, data_type: Literal["inputs", "puzzles", "examples", "answers"]
) -> Path:
    extension = "md" if data_type == "puzzles" else "txt"
    path = Path("data") / data_type / str(year) / f"{day:02}.{extension}"
    path.parent.mkdir(exist_ok=True)
    return path


def get_input_path(day: int, year: int) -> Path:
    return data_path(day, year, "inputs")


def get_puzzle_path(day: int, year: int) -> Path:
    return data_path(day, year, "puzzles")


def get_answer_path(day: int, year: int) -> Path:
    return data_path(day, year, "answers")


def get_example_path(day: int, year: int) -> Path:
    return data_path(day, year, "examples")


def get_solution_path(day: int, year: int) -> Path:
    path = Path("pycli") / "src" / f"year_{year}" / f"day_{day:02}.py"
    path.parent.mkdir(exist_ok=True)
    return path


def aoc(command):
    subprocess.run(f"aoc {command}", shell=True)


def parse_days(day: str) -> list[int]:
    if day.isdigit():
        return [int(day)]

    if day == "all":
        day = "1-25"
    start, end = map(int, day.split("-"))
    return list(range(start, end + 1))
