import importlib
import subprocess
import tomllib
from pathlib import Path

import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def main(day: int, part: int, use_example: bool = False, submit: bool = False):
    year = tomllib.loads(Path(".cargo/config.toml").read_text())["env"]["AOC_YEAR"]
    if use_example and submit:
        raise ValueError("Cannot use both --use-example and --submit")
    file_name = f"day_{day:02}"
    data_dir = "examples" if use_example else "inputs"
    data = Path("data") / data_dir / year / f"{day:02}.txt"
    package = importlib.import_module(f"src.bin.{file_name}")
    func = getattr(package, f"part_{part}")
    result = func(data.read_text())
    print(result)
    if submit:
        subprocess.run(f"aoc submit -y {year} -d {day:02} {part} {result}", shell=True)


if __name__ == "__main__":
    app()
