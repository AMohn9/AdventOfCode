from pathlib import Path


def parse_input_file(path: Path):
    dots = []
    folds = []

    with path.open('r') as f:
        for line in f:
            if "," in line:
                split_line = line.strip().split(",")
                dots.append((int(split_line[0]), int(split_line[1])))
            elif "fold" in line:
                split_line = line.strip().split(" ")[-1].split("=")
                folds.append((split_line[0], int(split_line[1])))

    return dots, folds


def add_mats(mat1, mat2):
    new_mat = []
    for row in range(len(mat1)):
        new_mat.append([
            mat1[row][col] or mat2[row][col]
            for col in range(len(mat1[0]))
        ])
    return new_mat


def fold_vertical(mat, y):
    # Split the matrix at the line
    mat1 = mat[:y]
    mat2 = mat[y+1:]

    # Reverse mat2 since the first line of mat2 will overlap the last line of mat1
    mat2 = mat2[::-1]

    # Resize them to the same size
    if len(mat1) != len(mat2):
        prefix = []
        for _ in range(abs(len(mat1) - len(mat2))):
            prefix.append([0 for _ in range(len(mat1[0]))])
        if len(mat1) < len(mat2):
            mat1 = prefix + mat1
        else:
            mat2 = prefix + mat2

    # Add and return
    return add_mats(mat1, mat2)


def fold_horizontal(mat, x):
    # Transverse, fold vertical, transverse
    t = list(zip(*mat))
    mat = fold_vertical(t, x)
    return list(zip(*mat))


def run(path: Path, max_folds: int) -> int:
    dots, folds = parse_input_file(path)

    # Init a matrix of the correct size with all false
    max_x = max(dots, key=lambda d: d[0])[0]
    max_y = max(dots, key=lambda d: d[1])[1]
    mat = [[False for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Set the values in dots to all true
    for x, y in dots:
        mat[y][x] = True

    # Do all the folds
    for fold_direction, fold_place in folds[:max_folds]:
        if fold_direction == "y":
            mat = fold_vertical(mat, fold_place)
        else:
            mat = fold_horizontal(mat, fold_place)

    # Print a readable version
    for line in mat:
        print(["#" if cell else "." for cell in line])

    return sum(mat[row][col] for row in range(len(mat)) for col in range(len(mat[0])))


def part_1(path: Path) -> int:
    return run(path, 1)


def part_2(path: Path) -> int:
    return run(path, 999)


if __name__ == "__main__":
    print(part_1(Path("day_13.txt")))
    print(part_2(Path("day_13.txt")))
