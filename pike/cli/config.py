import logging
from inspect import getmodule
from itertools import chain
from pathlib import Path
from typing import Generator, Optional, Set

from pike.cli.validate import Error, validate_tasks
from pike.task import Task
from pike.utils import import_file


class PikeFile:
    """
    Class to track the pikefile
    """

    DEFAULT_FILE_NAME = "pikefile.py"

    def __init__(self, path: Path):
        self.path = path
        self._tasks: Set[Task] = set()
        self._description: Optional[str] = None

    @classmethod
    def discover_path(cls, path: Path) -> Optional[Path]:
        """
        Discover a pikefile in the provided `path` or any of its parents
        """
        for candidate_dir in chain([path], path.parents):
            candidate_file = candidate_dir / cls.DEFAULT_FILE_NAME
            if candidate_file.is_file():
                return candidate_file
        return None

    @classmethod
    def discover(cls, path: Path) -> Optional["PikeFile"]:
        discovered_path = cls.discover_path(path)
        if discovered_path is not None:
            return cls(discovered_path)
        return discovered_path

    def _load(self):
        """
        Actually load the file
        """
        self._tasks.clear()
        pikefile_data = import_file(self.path)
        for name, val in pikefile_data.items():
            if name.startswith("_"):
                continue

            if not callable(val):
                continue

            if getmodule(val) is not None:
                continue

            self._tasks.add(Task.from_callable(val))

        if pikefile_data["__doc__"] is not None:
            self._description = pikefile_data["__doc__"].strip()

    @property
    def tasks(self) -> Set[Task]:
        if not self._tasks:
            self._load()

        return self._tasks

    @property
    def description(self) -> Optional[str]:
        if self._description is None:
            self._load()

        return self._description

    def validate(self) -> Generator[Error, None, None]:
        return validate_tasks(self.tasks)

    def validate_and_exit(self, level=logging.ERROR):
        critical_errors = [e for e in self.validate() if e.level >= level]
        if critical_errors:
            for error in critical_errors:
                error.show()
            exit(1)

    def get_task(self, name: str) -> Optional[Task]:
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.path == other.path
