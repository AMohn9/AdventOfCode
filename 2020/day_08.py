from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set


@dataclass
class Instruction:
    num: int
    type: str
    val: int


@dataclass
class Program:
    instructions: List[Instruction]


def parse_program(path: Path) -> Program:
    instructions = []
    with path.open('r') as f:
        for num, instruction in enumerate(f):
            type, value = instruction.split(" ")
            instructions.append(
                Instruction(
                    num,
                    type,
                    int(value)
                )
            )
    return Program(instructions)


def run_program(program: Program, must_valid_end: bool) -> Optional[int]:
    total = 0
    seen: Set[int] = set()

    instruction = program.instructions[0]

    def next_instruction() -> Optional[Instruction]:
        next_instruction_num = instruction.num + (instruction.val if instruction.type == "jmp" else 1)

        if next_instruction_num >= len(program.instructions):
            print(f"Instruction num {next_instruction_num} outside program")
            return None
        if next_instruction_num in seen:
            print(f"Already seen instruction num {next_instruction_num}")
            raise Exception()
        else:
            return program.instructions[next_instruction_num]

    while instruction:
        seen.add(instruction.num)
        if instruction.type == "acc":
            total += instruction.val
        try:
            instruction = next_instruction()
        except:
            if must_valid_end:
                return None
            return total

    return total


def part_1(path: Path) -> int:
    return run_program(parse_program(path), False)


def part_2(path: Path) -> int:
    program = parse_program(path)

    for instruction in program.instructions:
        if instruction.type == "acc":
            continue
        instruction.type = "jmp" if instruction.type == "nop" else "nop"
        ret = run_program(program, True)
        if ret:
            return ret
        instruction.type = "jmp" if instruction.type == "nop" else "nop"

    return 0


if __name__ == "__main__":
    print("Part 1: ", part_1(Path("day_08.txt")))
    print("Part 2: ", part_2(Path("day_08.txt")))
