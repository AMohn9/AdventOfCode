import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Set, Tuple


def parse_matrix(matrix_string: str) -> List[Set[int]]:
    return [
        [int(cell) for cell in row.strip().split()]
        for row in matrix_string.split("\n")
    ]


@dataclass
class Board:
    all_numbers: Set
    all_lines: List[Set[int]]
    seen_count: List[int]
    called: Set[int]

    def __init__(self, board_str: str):
        # All rows and columns
        self.all_lines = []
        matrix = parse_matrix(board_str)
        # Add rows
        for line in matrix:
            self.all_lines.append(set(line))
        # Add columns
        transposed_matrix = zip(*matrix)
        for line in transposed_matrix:
            self.all_lines.append(set(line))

        self.all_numbers = set(itertools.chain.from_iterable(self.all_lines))
        # How many we've seen on this row / column
        self.seen_count = [0 for _ in range(len(self.all_lines))]
        self.called = set()

    def get_uncalled_score(self) -> int:
        return sum(
            number for number in self.all_numbers
            if number not in self.called
        )

    def call(self, number: int) -> bool:
        if number not in self.all_numbers:
            return False

        self.called.add(number)
        for line_count, line in enumerate(self.all_lines):
            if number in line:
                self.seen_count[line_count] += 1
                if self.seen_count[line_count] == 5:
                    return True


def parse_input_file(path: Path) -> Tuple[List[int], List[Board]]:
    with path.open('r') as f:
        chunks = f.read().split("\n\n")
        numbers = [int(num) for num in chunks[0].split(",")]
        boards = [Board(chunk) for chunk in chunks[1:]]
    return numbers, boards


def find_winners(numbers: List[int], boards: List[Board]) -> Iterator[Tuple[Board, int]]:
    winners = []

    for number in numbers:
        for board in boards:
            if board in winners:
                continue

            if board.call(number):
                winners.append(board)
                yield board, number


def part_1(path: Path) -> int:
    numbers, boards = parse_input_file(path)
    winner, last_called = next(find_winners(numbers, boards))
    return winner.get_uncalled_score() * last_called


def part_2(path: Path) -> int:
    numbers, boards = parse_input_file(path)

    number_of_winners = 0

    for winner, last_called in find_winners(numbers, boards):
        number_of_winners += 1
        if number_of_winners == len(boards):
            return winner.get_uncalled_score() * last_called

    return 0


if __name__ == "__main__":
    print(part_1(Path("day_04.txt")))
    print(part_2(Path("day_04.txt")))
