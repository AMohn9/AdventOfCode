import operator
from collections import defaultdict
from itertools import takewhile
from pathlib import Path
from typing import Iterator, List, Tuple, Dict


def transpose(mat):
    return list(list(line) for line in zip(*mat))


def take_while_true(g):
    return takewhile(lambda x: x, g)


def read_file_as_ints(path: Path) -> Iterator[int]:
    # Each line is a new int
    with path.open('r') as f:
        yield from (int(line) for line in f.readlines())


def read_file_as_ints_2(path: Path) -> Iterator[int]:
    # Comma separated ints
    with path.open('r') as f:
        data = f.read().strip()
        return [int(i) for i in data.split(",")]


def read_file_to_int_matrix(path: Path) -> List[List[int]]:
    mat = []
    with path.open('r') as f:
        for line in f:
            mat.append([int(i) for i in line.strip()])
    return mat


def count_occurrences(ints: Iterator[int]) -> Dict[int, int]:
    d = defaultdict(int)
    for i in ints:
        d[i] += 1
    return d


def add_tuples(t1, t2):
    return tuple(map(operator.add, t1, t2))


def add_list_of_tuples(lst: List[Tuple[int, ...]]):
    return tuple(map(sum, zip(*lst)))


def bit_list_to_int(lst: List[int]) -> int:
    return int(''.join(str(bit) for bit in lst), 2)


