from pathlib import Path

from matrix import Mat
from utils import read_file_to_int_matrix


def part_1(path: Path) -> int:
    mat = Mat(read_file_to_int_matrix(path))

    def is_low_point():
        cell_val = mat.get_cell(row, col)
        for neighbor_row, neighbor_col in mat.cardinal_neighbors(row, col):
            if cell_val >= mat.get_cell(neighbor_row, neighbor_col):
                return False
        return True

    risk_total = 0
    for row in range(mat.row_count):
        for col in range(mat.col_count):
            if is_low_point():
                risk_total += mat.get_cell(row, col) + 1

    return risk_total


def part_2(path: Path) -> int:
    mat = Mat(read_file_to_int_matrix(path))

    # A mapping of cell (tuple row, col) to basin number
    cell_to_basin = {}
    # A mapping of basin number to a list of cells in that basin
    basin_dict = {}

    # Put each cell in it's own basin
    basin_count = 0
    for row in range(mat.row_count):
        for col in range(mat.col_count):
            if mat.get_cell(row, col) == 9:
                continue
            cell_to_basin[(row, col)] = basin_count
            basin_dict[basin_count] = [(row, col)]
            basin_count += 1

    def check_and_combine_basins(cell1, cell2):
        # If cell 1 and cell 2 are in different basins
        if cell2 in cell_to_basin and cell_to_basin[cell1] != cell_to_basin[cell2]:
            cell1_basin_num = cell_to_basin[cell1]
            cell2_basin_num = cell_to_basin[cell2]

            # Add everything in basin 2 into basin 1
            basin1 = basin_dict[cell1_basin_num]
            basin2 = basin_dict[cell2_basin_num]
            basin1.extend(basin2)

            # Update cell_to_basin that everything that was in basin 2 is  now in basin 1
            for cell_in_basin2 in basin2:
                cell_to_basin[cell_in_basin2] = cell1_basin_num

            # Remove basin 2
            basin_dict.pop(cell2_basin_num)
            return True
        return False

    # Keep combining until there're no more to combine
    combined_some = True
    while combined_some:
        combined_some = False

        for row in range(mat.row_count):
            for col in range(mat.col_count):
                if mat.get_cell(row, col) == 9:
                    continue

                for neighbor_row, neighbor_col in mat.cardinal_neighbors(row, col):
                    combined_some = check_and_combine_basins((row, col), (neighbor_row, neighbor_col)) or combined_some

    basins = list(basin_dict.values())
    basins.sort(key=len, reverse=True)

    return len(basins[0]) * len(basins[1]) * len(basins[2])


if __name__ == "__main__":
    print(part_1(Path("day_09.txt")))
    print(part_2(Path("day_09.txt")))
