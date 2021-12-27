from pathlib import Path

from utils import take_while_true, transpose


def parse_input_file(path: Path):
    with path.open('r') as f:
        mat = [[c for c in line.strip()] for line in f]
    return mat


def move_line_right(line, target_character):
    new_line = [i for i in line]
    place = -1 * len(line)
    while place < 0:
        if line[place] == target_character and line[place + 1] == ".":
            new_line[place] = "."
            new_line[place + 1] = target_character
            place += 2
        else:
            place += 1
    return new_line


def move_matrix_right(mat, target_character):
    return [
        move_line_right(line, target_character)
        for line in mat
    ]


def run_step(mat):
    mat = move_matrix_right(mat, ">")
    mat = transpose(mat)
    mat = move_matrix_right(mat, "v")
    return transpose(mat)


def part_1(path: Path) -> int:
    mat = parse_input_file(path)

    def run(mat):
        while True:
            new_mat = run_step(mat)
            yield new_mat != mat
            mat = new_mat

    return sum(take_while_true(run(mat))) + 1


def part_2(path: Path) -> int:
    return 0


if __name__ == "__main__":
    print(part_1(Path("day_25_test.txt")))
    print(part_2(Path("day_25.txt")))
