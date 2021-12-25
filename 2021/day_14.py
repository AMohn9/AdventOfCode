import re
from collections import defaultdict
from pathlib import Path

from more_itertools import sliding_window


def parse_input_file(path: Path):
    mappings = {}
    with path.open('r') as f:
        lines = f.readlines()

        for line in lines[2:]:
            split_line = line.strip().split(" -> ")
            mappings[split_line[0]] = split_line[1]

        return lines[0].strip(), mappings


def run(path: Path, steps: int) -> int:
    target, mappings = parse_input_file(path)

    for step_num in range(steps):
        for first_char, second_char in mappings.keys():
            # Use look arounds to put .s between every pair of values
            target = re.sub(rf"(?<={first_char})(?={second_char})", ".", target)
        # Replace .s with the correct characters
        for place, character in enumerate(target):
            if character == ".":
                insert_character = mappings[target[place-1] + target[place+1]]
                target = target[:place] + insert_character + target[place+1:]

    # Get the character counts
    unique_characters = set(target)
    counts = sorted([target.count(c) for c in unique_characters])

    return counts[-1] - counts[0]


def run2(path: Path, steps: int) -> int:
    target, mappings = parse_input_file(path)

    # NOTE: Everything in a size 2 sliding window is in mapping
    # Also, each new pair created by an insert is also in mapping
    # This means we don't have to keep the whole string, only a count of each pair in the mappings

    # Init the pair count with the input string
    pair_counts = defaultdict(int)
    for first, second in sliding_window(target, 2):
        pair_counts[(first, second)] += 1

    for _ in range(steps):
        new_pair_counts = defaultdict(int)
        # For each pair, break it into the two new pairs
        # Each of them occurs this many more times
        # e.g. if we have NC -> H and NC: 3
        # then in the new string we'll have NH: 3 and HC: 3
        for (first, second), count in pair_counts.items():
            insert_char = mappings[first + second]
            new_pair_counts[(first, insert_char)] += count
            new_pair_counts[(insert_char, second)] += count
        pair_counts = new_pair_counts

    # Count how many times each letter appears in the pairs
    letter_counts = defaultdict(int)
    for (first, second), count in pair_counts.items():
        letter_counts[first] += count
        letter_counts[second] += count

    # We're double counting because of overlaps, so divide
    for letter, count in letter_counts.items():
        # Plus one handles the edges of the string
        letter_counts[letter] = (count + 1) // 2

    counts = sorted(letter_counts.values())
    return counts[-1] - counts[0]


def part_1(path: Path) -> int:
    return run2(path, 10)


def part_2(path: Path) -> int:
    return run2(path, 40)


if __name__ == "__main__":
    print(part_1(Path("day_14.txt")))
    print(part_2(Path("day_14.txt")))
