from pathlib import Path
from typing import Dict, Iterator, Set, Tuple

from utils import add_list_of_tuples, read_file_as_ints

from more_itertools import sliding_window


def parse_input_file(path: Path) -> Iterator[Tuple[int, int]]:
    directions = {
        'up': (0, -1),
        'down': (0, 1),
        'forward': (1, 0),
    }
    with path.open('r') as f:
        for line in f:
            direction, distance = line.split(' ')
            yield tuple(int(distance) * d for d in directions[direction])


def part_1(path: Path) -> int:
    movements = parse_input_file(path)
    x, y = add_list_of_tuples(movements)
    return x * y


def part_2(path: Path) -> int:
    x, y, aim = 0, 0, 0
    for movement in parse_input_file(path):
        aim += movement[1]
        x += movement[0]
        y += movement[0] * aim
    return x * y


if __name__ == "__main__":
    print(part_1(Path("day_02.txt")))
    print(part_2(Path("day_02.txt")))
