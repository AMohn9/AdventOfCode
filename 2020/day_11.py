from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

path = Path("day_11.txt")
max_x = 11
max_y = 10


def read_seats() -> Tuple[Set[Tuple], Dict[Tuple, bool]]:
    occupied_mapping = {
        "L": False,
        "#": True,
    }

    seat_map = {}
    all_seats = set()
    with path.open("r") as f:
        for seat_line_num, seat_line in enumerate(f):
            for seat_num, seat in enumerate(seat_line):
                all_seats.add((seat_line_num, seat_num))
                if seat in occupied_mapping:
                    seat_map[(seat_line_num, seat_num)] = occupied_mapping[seat]

    return all_seats, seat_map


def build_seat_graph(seat_map: Dict[Tuple, bool]) -> Dict[Tuple, List[Tuple]]:
    seat_graph = defaultdict(list)

    for seat in seat_map.keys():
        for x_diff in (-1, 0, 1):
            for y_diff in (-1, 0, 1):
                if x_diff == y_diff == 0:
                    continue
                potential_seat = (seat[0]+x_diff, seat[1]+y_diff)
                if potential_seat in seat_map:
                    seat_graph[seat].append(potential_seat)

    return seat_graph


def part_1() -> int:
    all_seats, seat_map = read_seats()
    seat_graph = build_seat_graph(seat_map)

    def occupied_next_to() -> int:
        return sum(seat_map[next_to] for next_to in seat_graph[seat])

    changed = True
    while changed:
        to_change_lst = []
        for seat, occupied in seat_map.items():
            if not occupied and occupied_next_to() == 0:
                to_change_lst.append(seat)
            if occupied and occupied_next_to() >= 4:
                to_change_lst.append(seat)

        changed = len(to_change_lst) > 0
        for to_change in to_change_lst:
            seat_map[to_change] = not seat_map[to_change]

    return sum(seat_map.values())


def build_seat_graph_2(all_seats, seat_map: Dict[Tuple, bool]) -> Dict[Tuple, List[List[Tuple]]]:
    seat_graph = defaultdict(list)

    def visible(nexty) -> List[Tuple]:
        visible_lst = []
        visible_seat = nexty(seat)
        while visible_seat in all_seats:
            if visible_seat in seat_map:
                visible_lst.append(visible_seat)
            visible_seat = nexty(visible_seat)
        return visible_lst

    for seat in seat_map.keys():
        for x_diff in (-1, 0, 1):
            for y_diff in (-1, 0, 1):
                if not (x_diff or y_diff):
                    continue
                seat_graph[seat].append(visible(lambda s: (s[0]+x_diff, s[1]+y_diff)))

    return seat_graph


def build_seat_graph_3(all_seats, seat_map: Dict[Tuple, bool]) -> Dict[Tuple, List[Tuple]]:
    seat_graph = defaultdict(list)

    def next_visible(nexty) -> Optional[Tuple]:
        visible_seat = nexty(seat)
        while visible_seat in all_seats and visible_seat not in seat_map:
            visible_seat = nexty(visible_seat)
        if visible_seat in seat_map:
            return visible_seat
        return None

    for seat in seat_map.keys():
        for x_diff in (-1, 0, 1):
            for y_diff in (-1, 0, 1):
                if not (x_diff or y_diff):
                    continue
                visible = next_visible(lambda s: (s[0]+x_diff, s[1]+y_diff))
                if visible:
                    seat_graph[seat].append(visible)

    return seat_graph


def print_seat_map(seat_map):
    mapping = {
        False: "L",
        True: "#"
    }
    for line in range(10):
        s = ""
        for col in range(10):
            seat = (line, col)
            if seat in seat_map:
                s += mapping[seat_map[seat]]
            else:
                s += "."
        print(s)


def part_2() -> int:
    all_seats, seat_map = read_seats()
    seat_graph = build_seat_graph_3(all_seats, seat_map)

    def occupied_next_to_2() -> int:
        return sum(seat_map[next_to] for next_to in seat_graph[seat])

    changed = True
    while changed:
        to_change_lst = []
        for seat, occupied in seat_map.items():
            if not occupied and occupied_next_to_2() == 0:
                to_change_lst.append(seat)
            if occupied and occupied_next_to_2() >= 5:
                to_change_lst.append(seat)

        changed = len(to_change_lst) > 0
        for to_change in to_change_lst:
            seat_map[to_change] = not seat_map[to_change]

    return sum(seat_map.values())


if __name__ == "__main__":
    print("Part 1: ", part_1())
    print("Part 2: ", part_2())
