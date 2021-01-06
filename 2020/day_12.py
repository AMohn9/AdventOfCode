from pathlib import Path
from typing import List, Tuple

path = Path("day_12.txt")

action_mapping = {
    "N": (0, 1, 0),
    "E": (1, 0, 0),
    "S": (0, -1, 0),
    "W": (-1, 0, 0),
    "F": (1, 1, 0),
    "L": (0, 0, -1),
    "R": (0, 0, 1),
}


def tuple_multiple(t: Tuple, s: int) -> Tuple:
    return tuple(s * x for x in t)


def tuple_add(t1: Tuple, t2: Tuple) -> Tuple:
    return tuple(sum(x) for x in zip(t1, t2))


def read_directions() -> List[Tuple[int, int, int]]:
    with path.open("r") as f:
        return [tuple_multiple(action_mapping[line[0]], int(line[1:])) for line in f]


def part_1() -> int:
    state = (0, 0, 90)

    for action in read_directions():
        print(state, action)
        if action[0] and action[0] == action[1]:
            if state[2] == 0:
                state = tuple_add(state, (0, action[1], 0))
            if state[2] == 90:
                state = tuple_add(state, (action[1], 0, 0))
            if state[2] == 180:
                state = tuple_add(state, (0, -1 * action[1], 0))
            if state[2] == 270:
                state = tuple_add(state, (-1 * action[1], 0, 0))
        else:
            state = tuple_add(state, action)
            state = (state[0], state[1], state[2] % 360)

    print(state)
    return abs(state[0]) + abs(state[1])


def part_2() -> int:
    return 0


if __name__ == "__main__":
    print("Part 1: ", part_1())
    print("Part 2: ", part_2())
