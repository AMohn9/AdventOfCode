import copy
from pathlib import Path
from typing import Dict, Iterator, List, Set, Tuple

from utils import add_list_of_tuples, bit_list_to_int

from more_itertools import sliding_window


def parse_input_file(path: Path) -> Iterator[Tuple[int, int]]:
    with path.open('r') as f:
        for line in f:
            yield tuple(int(bit) for bit in list(line.strip()))


def part_1(path: Path) -> int:
    all_lines = list(parse_input_file(path))

    # The most common in each position will be rounded average for that position
    # e.g. if we had 7 elements, and a sum of 4, then 4/7 > 50%, so 1 is the most common
    count = len(all_lines)
    sum_of_lines = add_list_of_tuples(all_lines)

    gamma_list = [round(float(bit) / float(count) + .001) for bit in sum_of_lines]

    # Invert most common to find least common
    epsilon_list = [int(not bool(bit)) for bit in gamma_list]

    # Convert them to ints
    gamma = bit_list_to_int(gamma_list)
    epsilon = bit_list_to_int(epsilon_list)

    return gamma * epsilon


def get_last_in_common(options, prefer_most_common):
    options.sort(reverse=True)

    must_match = []

    for bit_place in range(len(options[0])):
        # The most common bit in place bit_place will be the bit in that place in the value at the mid point of
        # sorted options
        mid_point = options[(len(options) - 1) // 2]

        # If we want the most common, take it. Else flip it for the least common
        if prefer_most_common:
            must_match.append(mid_point[bit_place])
        else:
            must_match.append(int(not bool(mid_point[bit_place])))

        must_match_tuple = tuple(must_match)

        # Filter everything out that doesn't start with must_match_tuple
        options = list(filter(
            lambda option: option[:bit_place+1] == must_match_tuple,
            options
        ))

        # If we only have 1 left, return it
        if len(options) == 1:
            return options[0]


def part_2(path: Path) -> int:
    all_lines = list(parse_input_file(path))

    o2_generator = bit_list_to_int(get_last_in_common(all_lines, True))
    co2_scrubber = bit_list_to_int(get_last_in_common(all_lines, False))

    return o2_generator * co2_scrubber


if __name__ == "__main__":
    print(part_1(Path("day_03.txt")))
    print(part_2(Path("day_03.txt")))
