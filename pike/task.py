from inspect import getmodule
from pathlib import Path
from typing import Callable, NamedTuple, Set

from .utils import import_file


class Task(NamedTuple):
    name: str
    method: Callable


def load_tasks(pikefile: Path) -> Set[Task]:
    pikefile_data = import_file(pikefile)
    tasks = set()
    for name, val in pikefile_data.items():
        if name.startswith("_"):
            continue

        if not callable(val):
            continue

        if getmodule(val) is not None:
            continue

        tasks.add(Task(name=name, method=val))

    return tasks
