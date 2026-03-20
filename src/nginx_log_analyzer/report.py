from typing import Iterator
from pathlib import Path
import json

from .model import NormalizedLog


def console_(path: Path) -> None:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(data)


def file_(logs, path: Path) -> None:
    if isinstance(logs, dict):
        data = [logs]
    elif isinstance(logs, Iterator) and not isinstance(logs, (dict, str)):
        data = [log.to_dict() for log in logs]
    else:
        data = [logs.to_dict()]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
