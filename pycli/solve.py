import importlib
from pathlib import Path
from time import perf_counter

from rich import print as rprint

from .download import download
from .utils import aoc, data_path, get_answer_path


def run(day: int, year: int, part: int, example: bool, custom_file: Path | None):
    file_name = f"day_{day:02}"

    if custom_file is not None:
        data = custom_file
    else:
        data_dir = "examples" if example else "inputs"
        data = data_path(day, year, data_dir)
        if not data.is_file():
            download(day, year)

    package = importlib.import_module(f"pycli.src.year_{year}.{file_name}")
    func = getattr(package, f"part_{part}")
    return func(data.read_text(), example)


def solve(
    day: int,
    year: int,
    part: int,
    example: bool,
    check: bool,
    submit: bool,
    time: bool,
    custom_file: Path | None,
):
    assert day in set(range(1, 26)), f"'day' should be an int between 1 and 25, {day}"
    assert part in {1, 2}, f"'part' should be either 1 or 2, {part}"
    assert not (check and submit), "either check or submit"
    start = perf_counter()
    result = run(day, year, part, example, custom_file)
    duration = perf_counter() - start
    if time:
        print(f"time: {duration:.2f}")
    if check:
        answer = get_answer_path(day, year).read_text().strip().split("\n")[part - 1]
        if str(result) == answer:
            rprint(f"[green] {result} ✓[/green]")
        else:
            rprint(f"[red] {result}  [/red] != {answer}")

    else:
        print(result)
    if submit:
        aoc(f"submit -y {year} -d {day:02} {part} {result}")
        download(day, year)
