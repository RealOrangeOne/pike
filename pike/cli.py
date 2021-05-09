import argparse
import copy
from pathlib import Path
from typing import List, Optional, Tuple

from pike.registry import TaskRegistry
from pike.task import Parameter, Task
from pike.utils import noop

DEFAULT_FILE_NAME = "pikefile.py"


def contribute_parameter(parser: argparse.ArgumentParser, param: Parameter):
    argument_kwargs: dict = {}
    if param.param_type:
        argument_kwargs["type"] = param.param_type
    if param.description:
        argument_kwargs["help"] = param.description

    if param.has_default:
        argument_kwargs["help"] += " (default: %(default)s)"
        parser.add_argument(
            "--" + param.display_name,
            default=param.default,
            **argument_kwargs,
        )
    elif param.is_var_positional:
        del argument_kwargs["type"]
        parser.add_argument(param.display_name, nargs="*", **argument_kwargs)
    else:
        parser.add_argument(param.display_name, **argument_kwargs)


def get_file_argument(
    parser: argparse.ArgumentParser, argv: Optional[List[str]]
) -> Path:
    """
    Return the args values without doing any validation or usage display.
    """
    pre_parser = copy.deepcopy(parser)
    pre_parser.exit_on_error = False  # type:ignore
    pre_parser.print_usage = noop  # type:ignore
    pre_parser.print_help = noop  # type:ignore
    pre_parser.exit = noop  # type:ignore

    try:
        file_path = Path(pre_parser.parse_args(args=argv).file).resolve()
    except argparse.ArgumentError as e:
        # Throw a real error
        parser.error(str(e))

    # Check it's a file
    if not file_path.exists() or not file_path.is_file():
        parser.error(f"File {file_path} either doesn't exist or isn't a file.")

    return file_path


def get_parser_and_tasks(
    argv: Optional[List[str]] = None,
) -> Tuple[argparse.ArgumentParser, TaskRegistry]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file", "-f", default=DEFAULT_FILE_NAME, help="(default: %(default)s)"
    )
    parser.add_argument("--list", action="store_true", help="List tasks")
    parser.add_argument("--validate", action="store_true", help="Validate tasks")

    file = get_file_argument(parser, argv)

    subparsers = parser.add_subparsers(
        title="Tasks", description="Things to run", dest="task_name"
    )

    task_registry = TaskRegistry(file)

    task_registry.validate_and_exit()

    try:
        for task in task_registry.tasks:
            task_parser = subparsers.add_parser(task.name, description=task.description)
            for p in task.parameters:
                contribute_parameter(task_parser, p)
            task_parser.set_defaults(task=task)
    except SyntaxError as e:
        parser.error(f"Syntax error in file: {e}")

    return parser, task_registry


def run_task(task: Task, args: argparse.Namespace):
    task_args = []
    task_kwargs = {}
    for p in task.parameters:
        arg_value = getattr(args, p.name)
        if p.is_var_positional:
            task_args.extend(arg_value)
        else:
            task_kwargs[p.name] = arg_value

    task.method(*task_args, **task_kwargs)


def main():
    parser, task_registry = get_parser_and_tasks()
    args = parser.parse_args()

    if args.list:
        print(" ".join([task.name for task in task_registry.tasks]))
    elif args.validate:
        task_registry.validate_and_exit(level=0)
    elif getattr(args, "task", None):
        run_task(args.task, args)
    else:
        parser.print_help()
