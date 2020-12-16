from math import prod
from pathlib import Path
from typing import List, Tuple


def part_1(path: Path, x_rate: int, y_rate: int) -> int:
    with path.open('r') as f:
        return sum(
            line[(line_num // y_rate * x_rate) % 31] == '#'
            for line_num, line in enumerate(f)
            if line_num % y_rate == 0
        )


def part_2(path: Path, rates: List[Tuple[int, int]]) -> int:
    return prod(
        part_1(path, *rate)
        for rate in rates
    )


if __name__ == "__main__":
    print(part_1(Path("day_03.txt"), 3, 1))
    print(
        part_2(
            Path("day_03.txt"),
            [
                (1, 1),
                (3, 1),
                (5, 1),
                (7, 1),
                (1, 2),
            ]
        )
    )
