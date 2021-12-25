import bisect
import time
from pathlib import Path
from typing import Tuple, List

from matrix import Mat
from utils import read_file_to_int_matrix


def dijkstra(mat: Mat, source: Tuple[int, int], target: Tuple[int, int]) -> List[Tuple[int, int]]:
    distances = {}
    prev = {}
    q = []

    for row in range(mat.row_count):
        for col in range(mat.col_count):
            prev[(row, col)] = None
            if (row, col) != source:
                distances[(row, col)] = float('inf')
                q.append((float('inf'), (row, col)))
            else:
                distances[source] = 0
                q.append((0, (row, col)))

    q.sort()
    seen = set()

    q_place = 0
    while q_place != len(q):
        _, u = q[q_place]
        seen.add(u)
        q_place += 1

        if u == target:
            break

        for v in mat.cardinal_neighbors(*u):
            if v in seen:
                continue

            alt = distances[u] + mat.get_cell(*v)
            if alt < distances[v]:
                distances[v] = alt
                prev[v] = u

                # Update v in q, maintaining sorted
                bisect.insort(q, (alt, v))

    s = []
    u = target
    if prev[u] or u == source:
        while u:
            s.append(u)
            u = prev[u]

    return s[::-1]


def extend_mat(orig_mat: List[List[int]]):
    mat = []
    for line in orig_mat:
        to_add = []
        to_add.extend(line)

        new_line = line
        for right in range(1, 5):
            new_line = [(i % 9) + 1 for i in new_line]
            to_add.extend(new_line)
        mat.append(to_add)

    last_added = mat
    for down in range(1, 5):
        to_add = []
        for line in last_added:
            to_add.append([(i % 9) + 1 for i in line])
        mat.extend(to_add)
        last_added = to_add

    return mat


def part_1(path: Path) -> int:
    mat = Mat(read_file_to_int_matrix(path))
    target = (mat.row_count - 1, mat.col_count - 1)

    return sum(mat.get_cell(*cell) for cell in dijkstra(mat, (0, 0), target)[1:])


def part_2(path: Path) -> int:
    start = time.time()
    mat = read_file_to_int_matrix(path)
    mat = Mat(extend_mat(mat))
    target = (mat.row_count - 1, mat.col_count - 1)
    answer = sum(mat.get_cell(*cell) for cell in dijkstra(mat, (0, 0), target)[1:])
    print(time.time() - start)
    return answer


if __name__ == "__main__":
    print(part_1(Path("day_15.txt")))
    print(part_2(Path("day_15.txt")))
