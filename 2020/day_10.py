from pathlib import Path
from typing import Iterator


def read_file_as_ints(path: Path) -> Iterator[int]:
    with path.open("r") as f:
        yield from (int(line) for line in f.readlines())


def part_1(path: Path) -> int:
    numbers = sorted(list(read_file_as_ints(path)))
    numbers.append(numbers[-1] + 3)
    numbers.insert(0, 0)

    differences = [numbers[i] - numbers[i - 1] for i in range(1, len(numbers))]

    return differences.count(1) * differences.count(3)


def part_2(path: Path) -> int:
    numbers = sorted(read_file_as_ints(path), reverse=True)
    numbers.append(0)

    counts = {numbers[0]: 1}
    for num in numbers[1:]:
        counts[num] = sum(counts.get(num + jump_size, 0) for jump_size in (1, 2, 3))

    return counts[0]


if __name__ == "__main__":
    print("Part 1: ", part_1(Path("day_10.txt")))
    print("Part 2: ", part_2(Path("day_10.txt")))
