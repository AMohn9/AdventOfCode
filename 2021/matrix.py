from dataclasses import dataclass
from typing import List, Iterator, Tuple


@dataclass
class Mat:
    cells: List[List[int]]

    @property
    def row_count(self):
        return len(self.cells)

    @property
    def col_count(self):
        return len(self.cells[0])

    def get_cell(self, row, col) -> int:
        return self.cells[row][col]

    def set_cell(self, row, col, value) -> None:
        self.cells[row][col] = value

    def add(self, row, col, value) -> int:
        self.cells[row][col] += value
        return self.cells[row][col]

    def cardinal_neighbors(self, row, col) -> Iterator[Tuple[int, int]]:
        if row > 0:
            yield row-1, col
        if row < self.row_count - 1:
            yield row+1, col
        if col > 0:
            yield row, col-1
        if col < self.col_count - 1:
            yield row, col+1

    def all_neighbors(self, row, col) -> Iterator[Tuple[int, int]]:
        yield from self.cardinal_neighbors(row, col)

        if row > 0 and col > 0:
            yield row-1, col-1
        if row > 0 and col < self.col_count - 1:
            yield row - 1, col + 1
        if row < self.row_count - 1 and col > 0:
            yield row + 1, col - 1
        if row < self.row_count - 1 and col < self.col_count - 1:
            yield row + 1, col + 1

    def __str__(self):
        ret = ""
        for line in self.cells[:-1]:
            ret += str(line) + "\n"
        ret += str(self.cells[-1])
        return ret