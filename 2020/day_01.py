from pathlib import Path
from typing import Dict, Iterator, Set, Tuple


def read_file_as_ints(path: Path) -> Iterator[int]:
    with path.open('r') as f:
        yield from (int(line) for line in f.readlines())


def part_1(path: Path) -> int:
    """
    Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.
    """
    expenses: Set[int] = set(read_file_as_ints(path))

    for expense in expenses:
        if 2020 - expense in expenses:
            return expense * (2020 - expense)


def part_2(path: Path) -> int:
    """
    Find three numbers in your expense report that meet the same criteria.
    """
    expenses: Set[int] = set(read_file_as_ints(path))

    summed_expenses: Dict[int, Tuple[int, int]] = {
        e1 + e2: (e1, e2) for e1 in expenses for e2 in expenses
    }

    for expense_sum, (expense1, expense2) in summed_expenses.items():
        if 2020 - expense_sum in expenses:
            return expense1 * expense2 * (2020 - expense_sum)


if __name__ == "__main__":
    print(part_1(Path("day_01.txt")))
    print(part_2(Path("day_01.txt")))
