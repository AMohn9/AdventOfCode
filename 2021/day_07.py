from pathlib import Path
from typing import Tuple

from utils import count_occurrences, read_file_as_ints_2


def part_1(path: Path) -> Tuple[int, int]:
    crab_positions = sorted(read_file_as_ints_2(path))
    min_crab_position, max_crab_position = crab_positions[0], crab_positions[-1]
    crab_position_dict = count_occurrences(crab_positions)
    print(crab_positions)
    print(crab_position_dict)
    print()

    crabs_to_the_left = {min_crab_position: 0}
    for position in range(min_crab_position + 1, max_crab_position + 1):
        crabs_to_the_left[position] = crabs_to_the_left[position-1] + crab_position_dict[position-1]
    print(crabs_to_the_left)

    crabs_to_the_right = {max_crab_position: 0}
    for position in range(max_crab_position - 1, min_crab_position - 1, -1):
        crabs_to_the_right[position] = crabs_to_the_right[position + 1] + crab_position_dict[position + 1]
    print(crabs_to_the_right)
    print()

    move_to_the_right = {min_crab_position: 0}
    for position in range(min_crab_position + 1, max_crab_position + 1):
        move_to_the_right[position] = move_to_the_right[position-1] + crabs_to_the_left[position]
    print(move_to_the_right)

    move_to_the_left = {max_crab_position: 0}
    for position in range(max_crab_position - 1, min_crab_position - 1, -1):
        move_to_the_left[position] = move_to_the_left[position + 1] + crabs_to_the_right[position]
    print(move_to_the_left)

    min_position = min(
        range(min_crab_position, max_crab_position + 1),
        key=lambda p: move_to_the_right[p] + move_to_the_left[p]
    )
    return min_position, move_to_the_right[min_position] + move_to_the_left[min_position]


def part_2(path: Path) -> Tuple[int, int]:
    crab_positions = sorted(read_file_as_ints_2(path))
    min_crab_position, max_crab_position = crab_positions[0], crab_positions[-1]
    crab_position_dict = count_occurrences(crab_positions)
    print(crab_positions)
    print(crab_position_dict)
    print()

    crabs_to_the_left = {min_crab_position: 0}
    for position in range(min_crab_position + 1, max_crab_position + 1):
        crabs_to_the_left[position] = crabs_to_the_left[position-1] + crab_position_dict[position-1]
    print(crabs_to_the_left)

    crabs_to_the_right = {max_crab_position: 0}
    for position in range(max_crab_position - 1, min_crab_position - 1, -1):
        crabs_to_the_right[position] = crabs_to_the_right[position + 1] + crab_position_dict[position + 1]
    print(crabs_to_the_right)
    print()

    move_to_the_right = {min_crab_position: 0}
    for position in range(min_crab_position + 1, max_crab_position + 1):
        move_to_the_right[position] = move_to_the_right[position - 1]
        for position2 in range(min_crab_position, position):
            move_to_the_right[position] += (position - position2) * crab_position_dict[position2]
    print(move_to_the_right)

    move_to_the_left = {max_crab_position: 0}
    for position in range(max_crab_position - 1, min_crab_position - 1, -1):
        move_to_the_left[position] = move_to_the_left[position + 1]
        for position2 in range(max_crab_position, position, -1):
            move_to_the_left[position] += (position2 - position) * crab_position_dict[position2]
    print(move_to_the_left)

    min_position = min(
        range(min_crab_position, max_crab_position + 1),
        key=lambda p: move_to_the_right[p] + move_to_the_left[p]
    )
    return min_position, move_to_the_right[min_position] + move_to_the_left[min_position]


if __name__ == "__main__":
    print(part_1(Path("day_07.txt")))
    print(part_2(Path("day_07.txt")))
