from pathlib import Path
from typing import Iterator


def read_file_to_ints(path: Path) -> Iterator[int]:
    with path.open('r') as f:
        yield from (int(line) for line in f.readlines())
