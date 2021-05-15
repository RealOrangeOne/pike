from pathlib import Path

import pytest

from pike.cli.config import PikeFile
from pike.task import Task


def test_lazy_tasks(example_pikefile: Path):
    config = PikeFile(example_pikefile)

    assert len(config._tasks) == 0
    assert len(config.tasks) == 2
    assert len(config._tasks) == 2


def test_validate(example_pikefile: Path):
    config = PikeFile(example_pikefile)

    errors = list(config.validate())
    assert len(errors) == 0


def test_validate_and_exit_success(example_pikefile: Path):
    config = PikeFile(example_pikefile)

    try:
        config.validate_and_exit()
    except SystemExit:
        pytest.fail()


def test_validate_and_exit_fail(example_pikefile: Path):
    config = PikeFile(example_pikefile)

    def task_callable(arg1: example_pikefile):  # type:ignore[valid-type]
        pass

    config._tasks.add(Task.from_callable(task_callable))

    with pytest.raises(SystemExit):
        config.validate_and_exit()


def test_gets_task(example_pikefile: Path):
    config = PikeFile(example_pikefile)

    task = config.get_task("do-thing")
    assert task is not None

    assert task.name == "do-thing"
    assert task.parameters[0].name == "thing"


def test_wrapped_task(example_pikefile: Path):
    config = PikeFile(example_pikefile)

    task = config.get_task("wrapped-task")
    assert task is not None

    assert len(task.parameters) == 1
    assert task.parameters[0].name == "thing"