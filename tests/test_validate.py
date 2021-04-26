import logging

from pike.task import Task
from pike.validate import validate_task, validate_tasks


def test_valid_task():
    def task_callable():
        pass

    task = Task.from_callable(task_callable)

    errors = list(validate_task(task))

    assert len(errors) == 0


def test_invalid_param_type():
    def task_callable(arg1: validate_task):  # type:ignore[valid-type]
        pass

    task = Task.from_callable(task_callable)

    errors = list(validate_task(task))

    assert len(errors) == 1
    error = errors[0]

    assert error.task_name == task.name
    assert error.message == f"Argument arg1 is of invalid type {validate_task}"
    assert error.level == logging.ERROR


def test_different_default_type():
    def task_callable(arg1: int = "1"):  # type:ignore[assignment]
        pass

    task = Task.from_callable(task_callable)

    errors = list(validate_task(task))

    assert len(errors) == 1
    error = errors[0]

    assert error.task_name == task.name
    assert error.message == "Default value of arg1 (1) doesn't match its type int"
    assert error.level == logging.WARNING


def test_duplicate_named_tasks():
    def task_CALLABLE():
        pass

    def TASK_callable():
        pass

    task_1 = Task.from_callable(task_CALLABLE)
    task_2 = Task.from_callable(TASK_callable)

    errors = list(validate_tasks({task_1, task_2}))

    assert len(errors) == 1
    error = errors[0]

    assert error.task_name is None
    assert error.message == "Found 2 tasks with name 'task-callable'"
    assert error.level == logging.WARNING
