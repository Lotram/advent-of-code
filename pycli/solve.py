import importlib
from time import perf_counter

from .download import download
from .utils import aoc, data_path


def run(day: int, year: int, part: int, example: bool):
    file_name = f"day_{day:02}"
    data_dir = "examples" if example else "inputs"
    data = data_path(day, year, data_dir)
    if not data.is_file():
        download(day, year)
    package = importlib.import_module(f"src.bin.year_{year}.{file_name}")
    func = getattr(package, f"part_{part}")
    return func(data.read_text(), example)


def solve(day: int, year: int, part: int, example: bool, submit: bool, time: bool):
    assert day in set(range(1, 26)), f"'day' should be an int between 1 and 25, {day}"
    assert part in {1, 2}, f"'part' should be either 1 or 2, {part}"
    start = perf_counter()
    result = run(day, year, part, example)
    duration = perf_counter() - start
    if time:
        print(f"time: {duration:.2f}")
    print(result)
    if submit:
        aoc(f"submit -y {year} -d {day:02} {part} {result}")
