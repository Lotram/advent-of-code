from collections import deque


def part_1(text, example: bool = False):
    queue = deque(range(1, 1 + int(text.strip())))
    while len(queue) > 2:
        queue.append(queue.popleft())
        queue.popleft()

    result = queue[0]
    return result


def part_2(text, example: bool = False):
    count = int(text.strip())
    queue_1 = deque(range(1, 1 + count // 2))
    queue_2 = deque(range(1 + count // 2, 1 + count))
    while len(queue_2) > 1:
        queue_2.append(queue_1.popleft())
        queue_2.popleft()
        if len(queue_1) < len(queue_2) - 1:
            queue_1.append(queue_2.popleft())

    result = queue_1[0]
    return result
