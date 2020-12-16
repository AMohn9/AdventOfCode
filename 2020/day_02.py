from pathlib import Path
from typing import Tuple

from pydantic import BaseModel


class PasswordPolicy(BaseModel):
    value_1: int
    value_2: int
    letter: str

    @classmethod
    def parse(cls, policy_str: str):
        count_range, letter = policy_str.split(" ")
        value_1, value_2 = count_range.split("-")
        return PasswordPolicy(
            value_1=value_1,
            value_2=value_2,
            letter=letter,
        )


def parse_line(line: str) -> Tuple[PasswordPolicy, str]:
    policy, password = line.split(": ")
    return PasswordPolicy.parse(policy), password


def check_validity_part_1(policy: PasswordPolicy, password: str) -> bool:
    """
    A password is valid if there are at least value_1 and at most value_2 instances of letter in the password.
    """
    return policy.value_1 <= password.count(policy.letter) <= policy.value_2


def part_1(path: Path) -> int:
    """
    How many passwords are valid according to their policies?
    """
    with path.open("r") as f:
        return sum(check_validity_part_1(*parse_line(line)) for line in f)


def check_validity_part_2(policy: PasswordPolicy, password: str) -> bool:
    """
    A password is valid if the letter at value_1 xor value_2 is 'letter' (not zero indexed)
    """
    return (policy.letter == password[policy.value_1 - 1]) != (
        policy.letter == password[policy.value_2 - 1]
    )


def part_2(path: Path) -> int:
    """
    How many passwords are valid according to their policies?
    """
    with path.open("r") as f:
        return sum(check_validity_part_2(*parse_line(line)) for line in f)


if __name__ == "__main__":
    print(part_1(Path("day_02.txt")))
    print(part_2(Path("day_02.txt")))
