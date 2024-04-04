from typing import Annotated, Optional

import typer

from pycli.download import download as _download
from pycli.scaffold import scaffold as _scaffold
from pycli.solve import solve as _solve
from pycli.utils import get_solution_path

app = typer.Typer(no_args_is_help=True)

YEAR: None | int = 2015

Year = Annotated[Optional[int], typer.Option("--year", "-y")]


@app.command()
def solve(
    day: Annotated[str, typer.Argument()],
    part: Annotated[Optional[int], typer.Option("--part", "-p")] = None,
    year: Year = YEAR,
    example: Annotated[bool, typer.Option("--example", "-e")] = False,
    submit: Annotated[bool, typer.Option()] = False,
    time: Annotated[bool, typer.Option("--time", "-t")] = False,
):
    if example and submit:
        raise ValueError("Cannot use both --example and --submit")

    assert year is not None

    if day == "all":
        day = "1-25"

    if day.isdigit():
        assert part is not None
        _solve(int(day), year, part, example, submit, time)

    else:
        start, end = map(int, day.split("-"))
        errors = []
        for _day in range(start, end + 1):
            for _part in [1, 2]:
                path = get_solution_path(_day, year)
                if path.is_file():
                    print(f"day {_day:02} - {_part}")
                    try:
                        _solve(_day, year, _part, example, submit=False, time=time)
                    except Exception as error:
                        print(f"Error: {error}")
                        errors.append((_day, _part))
                    print()

        if errors:
            print(f"Encountered some errors: {errors}")


@app.command()
def download(
    day: Annotated[int, typer.Argument()],
    year: Year = YEAR,
):
    assert year is not None
    _download(day, year)


@app.command()
def scaffold(day: Annotated[int, typer.Argument()], year: Year = YEAR):
    assert year is not None
    _scaffold(day, year)


if __name__ == "__main__":
    app()
