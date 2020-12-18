from pathlib import Path
from typing import List


def parse_groups(path: Path) -> List[str]:
    with path.open("r") as f:
        return f.read().split("\n\n")


def part_1(path: Path) -> int:
    return sum(len(set(group.replace("\n", ""))) for group in parse_groups(path))


def part_2(path: Path) -> int:
    return sum(
        len(set.intersection(*(set(person) for person in group.splitlines())))
        for group in parse_groups(path)
    )


if __name__ == "__main__":
    print("Part 1: ", part_1(Path("day_06.txt")))
    print("Part 2: ", part_2(Path("day_06.txt")))
