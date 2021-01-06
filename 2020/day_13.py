from math import prod
from pathlib import Path
from typing import List, Tuple

path = Path("day_13.txt")


def read_schedule() -> Tuple[int, List[int]]:
    with path.open("r") as f:
        earliest_leave = int(next(f))
        times = []
        for time in next(f).split(","):
            if time == "x":
                times.append(None)
            else:
                times.append(int(time))
        return earliest_leave, times


def part_1() -> int:
    earliest_leave, times = read_schedule()

    min_bus_id, min_wait_time = 0, 999
    for time in times:
        if not time:
            continue
        wait_time = time - (earliest_leave % time)
        if wait_time < min_wait_time:
            min_bus_id, min_wait_time = time, wait_time

    return min_bus_id * min_wait_time


def chinese_remainder(n, a):
    total = 0
    product = prod(n)

    for n_i, a_i in zip(n, a):
        p = product // n_i
        total += a_i * invert_modulo(p, n_i) * p

    return total % product


# Extended Euclid
# Compute x, y s.t. a*x + b*y = gcd(a, b)
def extended_euclid(a: int, b: int) -> Tuple[int, int]:
    if b == 0:
        return 1, 0
    (x, y) = extended_euclid(b, a % b)
    k = a // b
    return y, x - k * y


# This function find the inverses of a
# I.e. find b s.t. b*a % n = 1
def invert_modulo(a: int, n: int) -> int:
    (b, x) = extended_euclid(a, n)
    if b < 0:
        b = (b % n + n) % n
    return b


def part_2() -> int:
    _, times = read_schedule()

    n, a = [], []
    for bus_num, bus_id in enumerate(times):
        if not bus_id:
            continue

        n.append(bus_id)
        a.append(-1 * bus_num)

    return chinese_remainder(n, a)


if __name__ == "__main__":
    print("Part 1: ", part_1())
    print("Part 2: ", part_2())
