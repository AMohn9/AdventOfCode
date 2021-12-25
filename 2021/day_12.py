from collections import defaultdict
from pathlib import Path
from typing import Tuple, Iterable


def parse_input_file(path: Path) -> Iterable[Tuple[str, str]]:
    with path.open('r') as f:
        for line in f:
            split_line = line.strip().split("-")
            yield split_line[0], split_line[1]


def part_1(path: Path) -> int:
    cave_graph = defaultdict(list)
    for cave1, cave2 in parse_input_file(path):
        cave_graph[cave1].append(cave2)
        cave_graph[cave2].append(cave1)

    # print(cave_graph)

    def is_small_cave(cave: str):
        return cave.lower() == cave

    paths = 0
    nodes = cave_graph["start"]
    current_path = ["start"]
    while len(nodes) > 0:
        node = nodes[-1]

        # print(f"Current path: {current_path}")
        # print(f"Nodes: {nodes}")
        # print(f"Current node: {node}")

        if node == "end":
            # Don't keep exploring under 'end'
            nodes.pop()
            paths += 1
            # print(f"Found a path to the end: {current_path + ['end']}")
            continue
        if node in current_path and (is_small_cave(node) or current_path[-1] == node):
            # This means we've explored everything under node and come back to it
            # so step back (off current path) then keep exploring
            if current_path[-1] == node:
                # print(f"Explored everything under {node}")
                nodes.pop()
                current_path.pop()
                continue

            if is_small_cave(node):
                # Can only visit a small cave once
                # print("Already been to this small cave, moving on")
                nodes.pop()
                continue
        else:
            current_path.append(node)
            nodes.extend(cave_graph[node])
        # print()

    return paths


def part_2(path: Path) -> int:
    cave_graph = defaultdict(list)
    for cave1, cave2 in parse_input_file(path):
        cave_graph[cave1].append(cave2)
        cave_graph[cave2].append(cave1)

    # print(cave_graph)

    def is_small_cave(cave: str):
        return cave.lower() == cave

    paths = 0
    nodes = cave_graph["start"]
    current_path = ["start"]
    has_small_visited_twice = False
    while len(nodes) > 0:
        # sleep(.1)
        node = nodes[-1]

        # print(f"Current path: {current_path}")
        # print(f"Nodes: {nodes}")
        # print(f"Current node: {node}")

        if node == "start":
            nodes.pop()
            continue
        if node == "end":
            # Don't keep exploring under 'end'
            nodes.pop()
            paths += 1
            # print(f"Found a path to the end: {current_path + ['end']}")
            continue
        if node in current_path and ((is_small_cave(node) and has_small_visited_twice) or current_path[-1] == node):
            # This means we've explored everything under node and come back to it
            # so step back (off current path) then keep exploring
            if current_path[-1] == node:
                # print(f"Explored everything under {node}")
                nodes.pop()
                current_path.pop()
                # If it's small and still in there, then this was the twice visited small cave
                if is_small_cave(node) and node in current_path:
                    has_small_visited_twice = False
                continue

            if is_small_cave(node) and has_small_visited_twice:
                # Can only visit a small cave once
                # print("Already been to this small cave, moving on")
                nodes.pop()
                continue
        else:
            if node in current_path and is_small_cave(node):
                has_small_visited_twice = True
            current_path.append(node)
            nodes.extend(cave_graph[node])

    return paths


if __name__ == "__main__":
    print(part_1(Path("day_12.txt")))
    print(part_2(Path("day_12.txt")))
