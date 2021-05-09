from pathlib import Path

import pytest

from pike.registry import TaskRegistry
from pike.task import Task


def test_lazy_tasks(example_pikefile: Path):
    registry = TaskRegistry(example_pikefile)

    assert len(registry._tasks) == 0
    assert len(registry.tasks) == 1
    assert len(registry._tasks) == 1


def test_validate(example_pikefile: Path):
    registry = TaskRegistry(example_pikefile)

    errors = list(registry.validate())
    assert len(errors) == 0


def test_validate_and_exit_success(example_pikefile: Path):
    registry = TaskRegistry(example_pikefile)

    try:
        registry.validate_and_exit()
    except SystemExit:
        pytest.fail()


def test_validate_and_exit_fail(example_pikefile: Path):
    registry = TaskRegistry(example_pikefile)

    def task_callable(arg1: example_pikefile):  # type:ignore[valid-type]
        pass

    registry._tasks.add(Task.from_callable(task_callable))

    with pytest.raises(SystemExit):
        registry.validate_and_exit()
