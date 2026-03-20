from pathlib import Path
from typing import Iterator


class Reader:
    def __init__(self, path: Path):
        self.path = path

    def load_file(self, path: Path) -> Iterator[str]:
        with open(path, errors="ignore") as file:
            for line in file:
                yield line.rstrip("\n")

    def load_path(self) -> Iterator[str]:
        if self.path.is_file():
            for line in self.load_file(self.path):
                yield line
        elif self.path.is_dir():
            for file in sorted(self.path.iterdir()):
                if file.is_file():
                    for line in self.load_file(file):
                        yield line
        else:
            raise FileNotFoundError(f"{self.path} not found")
