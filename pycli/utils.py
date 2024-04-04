import subprocess
from pathlib import Path
from typing import Literal


def data_path(
    day: int, year: int, data_type: Literal["inputs", "puzzles", "examples"]
) -> Path:
    extension = "md" if data_type == "puzzles" else "txt"
    path = Path("data") / data_type / str(year) / f"{day:02}.{extension}"
    path.parent.mkdir(exist_ok=True)
    return path


def get_input_path(day: int, year: int) -> Path:
    return data_path(day, year, "inputs")


def get_puzzle_path(day: int, year: int) -> Path:
    return data_path(day, year, "puzzles")


def get_example_path(day: int, year: int) -> Path:
    return data_path(day, year, "examples")


def get_solution_path(day: int, year: int) -> Path:
    path = Path("pycli") / "src" / "bin" / f"year_{year}" / f"day_{day:02}.py"
    path.parent.mkdir(exist_ok=True)
    return path


def aoc(command):
    subprocess.run(f"aoc {command}", shell=True)
