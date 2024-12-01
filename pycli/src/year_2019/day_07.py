import concurrent.futures
import queue
from itertools import permutations

from .intcode import IntCodeComputer


def part_1(text, example: bool = False):
    if example:
        text = (
            "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
        )
    result = -float("inf")
    codes = list(map(int, text.strip().split(",")))
    queues = [queue.Queue() for _ in range(6)]

    def amplifier(idx):
        computer = IntCodeComputer(
            codes=codes.copy(),
            input_queue=queues[idx],
            name=str(f"amp_{idx}"),
            output_queue=queues[(idx + 1)],
        )
        computer.run(block=True, timeout=5)

    for permutation in permutations(range(5)):
        for idx, value in enumerate(permutation):
            assert queues[idx].empty()
            queues[idx].put(value)

        queues[0].put(0)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(amplifier, range(5), timeout=6)
            result = max(result, queues[-1].get())

    return result


def part_2(text, example: bool = False):
    result = -float("inf")
    codes = list(map(int, text.strip().split(",")))
    queues = [queue.Queue() for _ in range(5)]

    def amplifier(idx):
        computer = IntCodeComputer(
            codes=codes.copy(),
            input_queue=queues[idx],
            name=str(f"amp_{idx}"),
            output_queue=queues[(idx + 1) % 5],
        )
        computer.run(block=True, timeout=5)

    for permutation in permutations(range(5, 10)):
        for idx, value in enumerate(permutation):
            assert queues[idx].empty()
            queues[idx].put(value)

        queues[0].put(0)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(amplifier, range(5), timeout=6)

        result = max(result, queues[0].get())

    return result
