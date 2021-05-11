import logging
from inspect import getmodule
from pathlib import Path
from typing import Generator, Set

from pike.task import Task
from pike.utils import import_file

from .validate import Error, validate_tasks


class TaskRegistry:
    """
    Keep track of tasks
    """

    _tasks: Set[Task]

    def __init__(self, pikefile: Path):
        self.pikefile = pikefile
        self._tasks = set()

    def _load(self):
        """
        Actually load the tasks
        """
        self._tasks.clear()
        pikefile_data = import_file(self.pikefile)
        for name, val in pikefile_data.items():
            if name.startswith("_"):
                continue

            if not callable(val):
                continue

            if getmodule(val) is not None:
                continue

            self._tasks.add(Task.from_callable(val))

    @property
    def tasks(self) -> Set[Task]:
        if not self._tasks:
            self._load()

        return self._tasks

    def validate(self) -> Generator[Error, None, None]:
        return validate_tasks(self.tasks)

    def validate_and_exit(self, level=logging.ERROR):
        critical_errors = [e for e in self.validate() if e.level >= level]
        if critical_errors:
            for error in critical_errors:
                error.show()
            exit(1)
