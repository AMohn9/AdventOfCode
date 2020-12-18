from pathlib import Path
from typing import Iterable


def seat_id_generator(path: Path) -> Iterable[int]:
    with path.open("r") as f:
        passes = f.read()
        passes = passes.replace("F", "0")
        passes = passes.replace("B", "1")
        passes = passes.replace("L", "0")
        passes = passes.replace("R", "1")

        yield from (int(line, 2) for line in passes.split("\n"))


def part_1(path: Path) -> int:
    return max(seat_id_generator(path))


def part_2(path: Path) -> int:
    all_seats = set(range(2 ** 10))
    not_seen = all_seats.difference(set(seat_id_generator(path)))

    for seat in not_seen:
        if (seat - 1 not in not_seen) and (seat + 1 not in not_seen):
            return seat


if __name__ == "__main__":
    print("Part 1: ", part_1(Path("day_05.txt")))
    print("Part 2: ", part_2(Path("day_05.txt")))
