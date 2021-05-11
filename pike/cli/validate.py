import logging
from collections import Counter
from typing import Generator, NamedTuple, Optional, Set

from pike.task import Parameter, Task


class Error(NamedTuple):
    task_name: Optional[str]
    message: str
    level: int

    def show(self):
        message = self.message

        if self.task_name:
            message = f"{self.task_name}: " + message

        logging.log(self.level, message)


def validate_tasks(tasks: Set[Task]) -> Generator[Error, None, None]:
    if not tasks:
        yield Error(None, "No tasks found", level=logging.WARNING)

    for task_name, counter in Counter([task.name for task in tasks]).items():
        if counter > 1:
            yield Error(
                None,
                f"Found {counter} tasks with name '{task_name}'",
                level=logging.WARNING,
            )

    for task in tasks:
        yield from validate_task(task)


def validate_task(task: Task) -> Generator[Error, None, None]:
    for param in task.parameters:
        yield from validate_parameter(task, param)


def validate_parameter(task: Task, param: Parameter) -> Generator[Error, None, None]:
    if param.param_type and not isinstance(param.param_type, type):
        yield Error(
            task.name,
            f"Argument {param.name} is of invalid type {param.param_type}",
            level=logging.ERROR,
        )

    if param.has_default and param.param_type:
        if not isinstance(param.default, param.param_type):
            yield Error(
                task.name,
                f"Default value of {param.name} ({param.default}) doesn't match its type {param.param_type.__name__}",
                level=logging.WARNING,
            )
