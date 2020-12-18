from pathlib import Path
from typing import Dict


def parse_bag_graph(path: Path) -> Dict[str, Dict[str, int]]:
    bag_graph = {}
    with path.open('r') as f:
        for line in f:
            # Remove trailing period
            bag, contains = line[:-2].split(" contain ")

            # Remove trailing s
            bag_graph[bag[:-1]] = {}

            for contained in contains.split(", "):
                if contained[0] == 'n':
                    continue

                count = int(contained.split(" ")[0])
                contained_bag = " ".join(contained.split(" ")[1:])

                # Remove trailing s
                if contained_bag[-1] == 's':
                    contained_bag = contained_bag[:-1]

                bag_graph[bag[:-1]][contained_bag] = count

    return bag_graph


def contains_gold(bag_color: str, bag_graph: Dict[str, Dict[str, int]]):
    if 'shiny gold bag' in bag_graph[bag_color]:
        return True
    return any(
        contains_gold(bag, bag_graph)
        for bag in bag_graph[bag_color].keys()
        if bag
    )


def part_1(path: Path) -> int:
    bag_graph = parse_bag_graph(path)
    return sum(
        contains_gold(bag, bag_graph)
        for bag in bag_graph.keys()
    )


counts: Dict[str, int] = {}


def count_contained_bags(bag_color: str, bag_graph: Dict[str, Dict[str, int]]) -> int:
    if bag_color not in counts:
        counts[bag_color] = 1 + sum(
            count * count_contained_bags(bag, bag_graph)
            for bag, count in bag_graph[bag_color].items()
        )

    return counts[bag_color]


def part_2(path: Path) -> int:
    bag_graph = parse_bag_graph(path)
    return count_contained_bags('shiny gold bag', bag_graph) - 1


if __name__ == "__main__":
    print("Part 1: ", part_1(Path("day_07.txt")))
    print("Part 2: ", part_2(Path("day_07.txt")))
