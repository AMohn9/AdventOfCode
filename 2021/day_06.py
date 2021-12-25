from pathlib import Path
from typing import Iterator

from utils import count_occurrences, read_file_as_ints_2


def process_fish(fishies: Iterator[int], days_to_run: int) -> int:
    fish_dict = count_occurrences(fishies)

    for _ in range(days_to_run):
        new_fish_dict = {8: fish_dict.get(0, 0)}

        for days_left in range(1, 9):
            new_fish_dict[days_left - 1] = fish_dict.get(days_left, 0)
        new_fish_dict[6] += fish_dict[0]

        fish_dict = new_fish_dict
    return sum(fish_dict.values())


def part_1(path: Path) -> int:
    return process_fish(read_file_as_ints_2(path), 80)


def part_2(path: Path) -> int:
    return process_fish(read_file_as_ints_2(path), 256)


if __name__ == "__main__":
    print(part_1(Path("day_06.txt")))
    print(part_2(Path("day_06.txt")))
