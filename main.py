import importlib
import subprocess
from pathlib import Path
from time import perf_counter

import tomllib
import typer

app = typer.Typer(no_args_is_help=True)


def run(year, day, part, example):
    file_name = f"day_{day:02}"
    data_dir = "examples" if example else "inputs"
    data = Path("data") / data_dir / year / f"{day:02}.txt"
    if not data.is_file():
        subprocess.run(f"cargo download {day}", shell=True)
    package = importlib.import_module(f"src.bin.year_{year}.{file_name}")
    func = getattr(package, f"part_{part}")
    return func(data.read_text())


def _main(year, day, part, example, submit, time):
    assert day in set(range(1, 26)), f"'day' should be an int between 1 and 25, {day}"
    assert part in {1, 2}, f"'part' should be either 1 or 2, {part}"
    start = perf_counter()
    result = run(year, day, part, example)
    duration = perf_counter() - start
    if time:
        print(f"time: {duration:.2f}")
    print(result)
    if submit:
        subprocess.run(f"aoc submit -y {year} -d {day:02} {part} {result}", shell=True)


@app.command()
def main(
    day: str,
    part: int = None,
    example: bool = False,
    submit: bool = False,
    time: bool = False,
):
    if example and submit:
        raise ValueError("Cannot use both --example and --submit")

    year = tomllib.loads(Path(".cargo/config.toml").read_text())["env"]["AOC_YEAR"]

    if day == "all":
        day = "1-25"

    if day.isdigit():
        _main(year, int(day), part, example, submit, time)

    else:
        start, end = map(int, day.split("-"))
        errors = []
        for _day in range(start, end + 1):
            for _part in [1, 2]:
                if Path(f"src/bin/year_{year}/day_{_day:02}.py").is_file():
                    print(f"day {_day:02} - {_part}")
                    try:
                        _main(year, _day, _part, example, False, time)
                    except Exception as error:
                        print(f"Error: {error}")
                        errors.append((_day, _part))
                    print()

        if errors:
            print(f"Encountered some errors: {errors}")


if __name__ == "__main__":
    app()
