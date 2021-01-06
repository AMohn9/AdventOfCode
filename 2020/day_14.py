import re
from dataclasses import dataclass
from pathlib import Path
from typing import List


path = Path("day_14.txt")


@dataclass
class MaskedSeries:
    mask: str
    mem_updates: dict


def process_mask(mask: str):
    mask_1 = mask.replace('1', '0').replace('X', '1')

    mask_2 = mask.replace('X', '0')

    return int(mask_1, 2), int(mask_2, 2)


def read_program() -> List[MaskedSeries]:
    series = []
    with path.open("r") as f:
        mask = ""
        mem_updates = {}
        for line in f:
            if "mask" in line:
                if mask:
                    series.append(MaskedSeries(
                        mask=mask,
                        mem_updates=mem_updates
                    ))
                    mem_updates = {}
                mask = line.split(" = ")[1].strip()
            else:
                location, value = re.match(r"mem\[(\d*)\] = (\d*)", line).groups()
                mem_updates[int(location)] = int(value)
    series.append(MaskedSeries(
        mask=mask,
        mem_updates=mem_updates
    ))
    return series


def part_1() -> int:
    program = read_program()

    mem_values = {}

    for series in program:
        # mask_1 limits to just the Xs, mask_2 adds the mask back in
        mask_1, mask_2 = process_mask(series.mask)

        for update_location, update_val in series.mem_updates.items():
            update_val &= mask_1
            update_val |= mask_2

            mem_values[update_location] = update_val

    return sum(mem_values.values())


def part_2() -> int:
    program = read_program()
    print(program)
    return 0


if __name__ == "__main__":
    print("Part 1: ", part_1())
    # print("Part 2: ", part_2())
