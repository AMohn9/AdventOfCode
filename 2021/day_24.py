from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, TypeVar, Union

B = TypeVar("B", bound=Union[int, str])


class InstructionType(Enum):
    inp = 1
    add = 2
    mul = 3
    div = 4
    mod = 5
    eql = 6


@dataclass
class Instruction:
    type: InstructionType
    a: str
    b: Optional[B]


@dataclass
class Computer:
    registers: Dict[str, int]
    instructions: List[Instruction]
    inputs: List[int]

    def run(self):
        for instruction in self.instructions:
            f = self.__getattribute__(instruction.type.name)
            f(instruction.a, instruction.b)
        return self.registers["z"] == 0

    def inp(self, register: str, _):
        self.registers[register] = self.inputs.pop(0)

    def add(self, register: str, to_add: B):
        if isinstance(to_add, int):
            self.registers[register] += to_add
        else:
            self.registers[register] += self.registers[to_add]

    def mul(self, register: str, to_mul: B):
        if isinstance(to_mul, int):
            self.registers[register] *= to_mul
        else:
            self.registers[register] *= self.registers[to_mul]

    def div(self, register: str, to_div: B):
        if isinstance(to_div, int):
            self.registers[register] //= to_div
        else:
            self.registers[register] //= self.registers[to_div]

    def mod(self, register: str, to_mod: B):
        if isinstance(to_mod, int):
            self.registers[register] %= to_mod
        else:
            self.registers[register] &= self.registers[to_mod]

    def eql(self, register: str, to_check: B):
        if isinstance(to_check, int):
            self.registers[register] = self.registers[register] == to_check
        else:
            self.registers[register] = self.registers[register] == self.registers[to_check]


def parse_input_file(path: Path) -> List[Instruction]:
    instructions = []
    with path.open('r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                parts.append('')
            elif parts[2].isnumeric() or "-" in parts[2]:
                parts[2] = int(parts[2])
            instructions.append(Instruction(InstructionType[parts[0]], parts[1], parts[2]))
    return instructions


def part_1(path: Path) -> int:
    instructions = parse_input_file(path)
    for n in range(100000000000000, 11111111111111, -1):
        if not n % 100000:
            print(n)
        inputs = [int(c) for c in str(n)]
        if 0 in inputs:
            continue
        c = Computer(
            {'w': 0, 'x': 0, 'y': 0, 'z': 0},
            instructions,
            inputs
        )
        if c.run():
            return n


def part_2(path: Path) -> int:
    return 0


if __name__ == "__main__":
    print(part_1(Path("day_24.txt")))
    print(part_2(Path("day_24.txt")))
