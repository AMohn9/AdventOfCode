from pathlib import Path
from typing import Iterator


def read_file_as_ints(path: Path) -> Iterator[int]:
    with path.open('r') as f:
        yield from (int(line) for line in f.readlines())


def part_1(path: Path) -> int:
    numbers = list(read_file_as_ints(path))
    preamble = set(numbers[:25])

    for remove_place, number in enumerate(numbers[25:]):
        for sum_candidate in preamble:
            if number - sum_candidate in preamble:
                break
        else:
            return number
        preamble.add(number)
        preamble.remove(numbers[remove_place])

    return 0


def part_2(path: Path) -> int:
    numbers = list(read_file_as_ints(path))
    bad = part_1(path)

    total = 0
    start_index = 0
    end_index = 0

    while total != bad:
        if total < bad:
            total += numbers[end_index]
            end_index += 1
        elif total > bad:
            total -= numbers[start_index]
            start_index += 1

    return min(numbers[start_index:end_index]) + max(numbers[start_index:end_index])


if __name__ == "__main__":
    print("Part 1: ", part_1(Path("day_09.txt")))
    print("Part 2: ", part_2(Path("day_09.txt")))
