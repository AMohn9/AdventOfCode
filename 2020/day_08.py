from pathlib import Path
from typing import List


def parse_groups(path: Path) -> List[str]:
    with path.open("r") as f:
        return f.read().split("\n\n")


def part_1(path: Path) -> int:
    return 0


def part_2(path: Path) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1: ", part_1(Path("day_08.txt")))
    print("Part 2: ", part_2(Path("day_08.txt")))
