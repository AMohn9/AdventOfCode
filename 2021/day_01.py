from pathlib import Path
from typing import Dict, Iterator, Set, Tuple

from utils import read_file_as_ints

from more_itertools import sliding_window


def count_sliding_window_increase(iterator: Iterator[int]):
    """
    Count how many times the iterator increases
    """
    return sum(
        first < second
        for first, second in sliding_window(iterator, 2)
    )


def part_1(path: Path) -> int:
    """
    Find the number of times the number increases
    """
    return count_sliding_window_increase(read_file_as_ints(path))


def part_2(path: Path) -> int:
    """
    Find how many times a sum of 3 increases
    """
    three_sliding_window = (
        sum(window)
        for window in sliding_window(read_file_as_ints(path), 3)
    )
    return count_sliding_window_increase(three_sliding_window)


if __name__ == "__main__":
    print(part_1(Path("day_01.txt")))
    print(part_2(Path("day_01.txt")))
