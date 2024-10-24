import re
from collections import Counter, defaultdict
from datetime import datetime


pattern = re.compile(r"\[(?P<dt>.*)\] (?P<message>.*)")


def get_asleep_minutes(text):
    lines = sorted(text.strip().split("\n"))
    guard = None
    asleep = False
    previous_dt = None
    asleep_minutes = defaultdict(list)
    for line in lines:
        dt_str, message = pattern.match(line).groups()
        dt = datetime.fromisoformat(dt_str)
        match message.split():
            case ["wakes", "up"]:
                assert asleep is True
                assert previous_dt.date() == dt.date()
                asleep_minutes[guard].extend(range(previous_dt.minute, dt.minute))
                asleep = False

            case ["falls", "asleep"]:
                assert asleep is False
                asleep = True

            case ["Guard", guard_id, "begins", "shift"]:
                assert asleep is False
                guard = int(guard_id[1:])
        previous_dt = dt
    return asleep_minutes


def part_1(text, example: bool = False):
    asleep_minutes = get_asleep_minutes(text)
    guard, minutes = max(asleep_minutes.items(), key=lambda item: len(item[1]))
    result = guard * Counter(minutes).most_common(1)[0][0]
    return result


def part_2(text, example: bool = False):
    asleep_minutes = get_asleep_minutes(text)
    [(max_minute, count)], guard = max(
        ((Counter(val).most_common(1), key) for key, val in asleep_minutes.items()),
        key=lambda item: item[0][0][1],
    )
    result = guard * max_minute
    return result
