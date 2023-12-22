import string
from itertools import count
from pathlib import Path

counter = count(1)
data = Path("data/day_3/data.txt").read_text()

values = {letter: next(counter) for letter in string.ascii_letters}
print(
    sum(
        values[(set(chars[: len(chars) // 2]) & set(chars[len(chars) // 2 :])).pop()]
        for chars in map(list, data.split("\n"))
    )
)
