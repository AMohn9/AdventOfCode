from itertools import permutations
from pathlib import Path


def parse_input_file(path: Path):
    with path.open('r') as f:
        for line in f:
            parts = line.strip().split(" | ")
            watched = parts[0].split(" ")
            written_down = parts[1].split(" ")
            yield watched, written_down


def part_1(path: Path) -> int:
    target_lengths = {2, 4, 3, 7}
    return sum(
        len(num) in target_lengths
        for _, written in parse_input_file(path)
        for num in written
    )


number_mappings = [
    {"a", "b", "c", "e", "f", "g"},
    {"c", "f"},
    {"a", "c", "d", "e", "g"},
    {"a", "c", "d", "f", "g"},
    {"b", "c", "d", "f"},
    {"a", "b", "d", "f", "g"},
    {"a", "b", "d", "e", "f", "g"},
    {"a", "c", "f"},
    {"a", "b", "c", "d", "e", "f", "g"},
    {"a", "b", "c", "d", "f", "g"},
]


def find_mapings(inputs):
    def works():
        for inp in inputs:
            really_turned_on = {mapping[c] for c in inp}
            if really_turned_on not in number_mappings:
                return False
        return True

    for p in permutations("abcdefg"):
        mapping = {k: v for k, v in zip(p, "abcdefg")}
        if works():
            return mapping


def part_2(path: Path) -> int:
    total = 0
    for inputs, outputs in parse_input_file(path):
        wire_mappings = find_mapings(inputs)
        output_digits = []
        for output in outputs:
            real_output = {wire_mappings[c] for c in output}
            output_digits.append(number_mappings.index(real_output))
        for digit_place, digit in enumerate(output_digits[::-1]):
            total += digit * (10 ** digit_place)
    return total


if __name__ == "__main__":
    print(part_1(Path("day_08.txt")))
    print(part_2(Path("day_08.txt")))
