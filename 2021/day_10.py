from collections import deque
from typing import Iterator
from pathlib import Path


INVALID_CHARACTER_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

ENDING_CHARACTER_SCORES = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

CLOSING_CHARACTERS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}


def read_input_file(path: Path) -> Iterator[str]:
    with path.open('r') as f:
        for line in f:
            yield line.strip()


def score_invalid_line(line: str) -> int:
    stack = deque()
    for character in line:
        if character in CLOSING_CHARACTERS:
            if len(stack) == 0 or stack.pop() != CLOSING_CHARACTERS[character]:
                return INVALID_CHARACTER_SCORES[character]
        else:
            stack.append(character)
    return 0


def complete_incomplete_line(line: str) -> int:
    stack = deque()
    for character in line:
        if character in CLOSING_CHARACTERS:
            if len(stack) == 0 or stack.pop() != CLOSING_CHARACTERS[character]:
                return 0
        else:
            stack.append(character)

    score = 0
    while len(stack) > 0:
        score *= 5
        score += ENDING_CHARACTER_SCORES[stack.pop()]
    return score


def part_1(path: Path) -> int:
    return sum(map(score_invalid_line, read_input_file(path)))


def part_2(path: Path) -> int:
    scores = list(
        filter(
            lambda x: x != 0,
            map(complete_incomplete_line, read_input_file(path))
        )
    )
    scores.sort()
    return scores[len(scores) // 2]


if __name__ == "__main__":
    print(part_1(Path("day_10.txt")))
    print(part_2(Path("day_10.txt")))
