from pathlib import Path
from typing import List, Tuple


def parse_passports(path: Path) -> List[str]:
    with path.open("r") as f:
        return f.read().split("\n\n")


def part_1(path: Path) -> int:
    necessary_fields = [
        "byr:",
        "iyr:",
        "eyr:",
        "hgt:",
        "hcl:",
        "ecl:",
        "pid:",
    ]
    return sum(
        all(field in passport for field in necessary_fields)
        for passport in parse_passports(path)
    )


def test_hgt(hgt: str) -> bool:
    if hgt[-2:] == "cm":
        return 150 <= int(hgt[:-2]) <= 193
    if hgt[-2:] == "in":
        return 59 <= int(hgt[:-2]) <= 76
    return False


def test_hcl(hcl: str) -> bool:
    if hcl[0] != '#':
        return False
    for letter in hcl[1:]:
        if not ((48 <= ord(letter) <= 57) or (97 <= ord(letter) <= 102)):
            return False
    return True


def part_2(path: Path) -> int:
    rules = {
        "byr": lambda x: 1920 <= int(x) <= 2002,
        "iyr": lambda x: 2010 <= int(x) <= 2020,
        "eyr": lambda x: 2020 <= int(x) <= 2030,
        "hgt": test_hgt,
        "hcl": test_hcl,
        "ecl": lambda x: x in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
        "pid": lambda x: len(x) == 9 and int(x),
    }
    count = 0
    for passport in parse_passports(path):
        passport = passport.replace("\n", " ")
        fields = {
            option.split(":")[0]: option.split(":")[1]
            for option in passport.split(" ")
        }
        for field, rule in rules.items():
            try:
                if not rule(fields[field]):
                    break
            except Exception:
                break
        else:
            count += 1

    return count


if __name__ == "__main__":
    print("Part 1: ", part_1(Path("day_04.txt")))
    print("Part 2: ", part_2(Path("day_04.txt")))
