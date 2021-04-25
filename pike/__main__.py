import argparse
import copy
from pathlib import Path
from typing import List, Optional

from pike.task import Parameter, load_tasks
from pike.utils import noop

DEFAULT_FILE_NAME = "pikefile.py"


def contribute_parameter(parser: argparse.ArgumentParser, param: Parameter):
    argument_kwargs: dict = {}
    if param.param_type:
        argument_kwargs["type"] = param.param_type

    if param.has_default:
        parser.add_argument(
            "--" + param.name,
            **argument_kwargs,
            default=param.default,
            help="(default: %(default)s)",
        )
    elif param.is_var_positional:
        parser.add_argument(param.name, nargs="*")
    else:
        parser.add_argument(param.name, **argument_kwargs)


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


def get_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file", "-f", default=DEFAULT_FILE_NAME, help="(default: %(default)s)"
    )

    file = get_file_argument(parser, argv)

    subparsers = parser.add_subparsers(
        title="Tasks", description="Things to run", dest="task_name"
    )

    try:
        for task in load_tasks(file):
            task_parser = subparsers.add_parser(task.name)
            for p in task.parameters:
                contribute_parameter(task_parser, p)
            task_parser.set_defaults(task=task)
    except SyntaxError as e:
        parser.error(f"Syntax error in file: {e}")

    return parser.parse_args(args=argv)


def main():
    args = get_args()
    print(args)


if __name__ == "__main__":
    main()
