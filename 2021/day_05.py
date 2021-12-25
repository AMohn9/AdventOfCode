from collections import defaultdict
from pathlib import Path
from typing import Iterator, Tuple

from utils import add_tuples


def parse_input_file(path: Path) -> Iterator[Tuple[Tuple[int, int], Tuple[int, int]]]:
    with path.open('r') as f:
        for line in f:
            start, end = line.strip().split(" -> ")
            (x1, y1), (x2, y2) = start.split(","), end.split(",")
            yield (int(x1), int(y1)), (int(x2), int(y2))


def compare_ints(a, b) -> int:
    if a < b:
        return 1
    if a == b:
        return 0
    if a > b:
        return -1


def get_direction(t1, t2):
    (x1, y1), (x2, y2) = t1, t2
    return compare_ints(x1, x2), compare_ints(y1, y2)


def count_dangerous_spots(sea_floor):
    return sum(
        cell_value > 1
        for cell_value in sea_floor.values()
    )


def part_1(path: Path) -> int:
    sea_floor = defaultdict(int)

    for start, end in parse_input_file(path):
        direction = get_direction(start, end)
        if direction[0] and direction[1]:
            continue

        while start != end:
            sea_floor[start] += 1
            start = add_tuples(start, direction)
        sea_floor[end] += 1

    return count_dangerous_spots(sea_floor)


def part_2(path: Path) -> int:
    sea_floor = defaultdict(int)

    for start, end in parse_input_file(path):
        direction = get_direction(start, end)

        while start != end:
            sea_floor[start] += 1
            start = add_tuples(start, direction)
        sea_floor[end] += 1

    return count_dangerous_spots(sea_floor)


if __name__ == "__main__":
    print(part_1(Path("day_05.txt")))
    print(part_2(Path("day_05.txt")))
