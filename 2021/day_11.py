from pathlib import Path
from typing import Set

from matrix import Mat
from utils import read_file_to_int_matrix


def flash(octos: Mat, row: int, col: int, flashed: Set) -> None:
    flashed.add((row, col))

    for neighbor_row, neighbor_col in octos.all_neighbors(row, col):
        new_val = octos.add(neighbor_row, neighbor_col, 1)

        if new_val == 10:
            flash(octos, neighbor_row, neighbor_col, flashed)


def process_step(octos: Mat) -> int:
    flashed = set()

    for row in range(octos.row_count):
        for col in range(octos.col_count):
            new_value = octos.add(row, col, 1)
            if new_value == 10:
                flash(octos, row, col, flashed)

    for row, col in flashed:
        octos.set_cell(row, col, 0)

    return len(flashed)


def part_1(path: Path) -> int:
    octos = Mat(read_file_to_int_matrix(path))

    return sum(process_step(octos) for _ in range(100))


def part_2(path: Path) -> int:
    octos = Mat(read_file_to_int_matrix(path))
    total = octos.row_count * octos.col_count

    step_num = 1
    while process_step(octos) != total:
        step_num += 1
    return step_num


if __name__ == "__main__":
    print(part_1(Path("day_11.txt")))
    print(part_2(Path("day_11.txt")))
