import argparse
import copy
from pathlib import Path
from typing import List, Optional, Tuple

from pike.task import Parameter
from pike.utils import noop

from .config import PikeFile


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
        file_argument = pre_parser.parse_args(args=argv).file
    except argparse.ArgumentError as e:
        # Throw a real error
        parser.error(str(e))

    if file_argument is None:
        # Not provided, discover
        file_path = PikeFile.discover_path(Path.cwd())
        if file_path is None:
            parser.error(
                f"Could not discover a {PikeFile.DEFAULT_FILE_NAME} in {str(Path.cwd())} or any of its parents"
            )
    else:
        file_path = Path(file_argument).resolve()
        # Check it's a file
        if not file_path.exists() or not file_path.is_file():
            parser.error(f"File {file_path} either doesn't exist or isn't a file.")

    return file_path


def get_parser_and_config(
    argv: Optional[List[str]] = None,
) -> Tuple[argparse.ArgumentParser, PikeFile]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file",
        "-f",
        help="(default: %(default)s)",
    )
    parser.add_argument("--list", action="store_true", help="List tasks")
    parser.add_argument("--validate", action="store_true", help="Validate tasks")

    file = get_file_argument(parser, argv)

    subparsers = parser.add_subparsers(
        title="Tasks", description="Things to run", dest="task_name"
    )

    config = PikeFile(file)

    config.validate_and_exit()

    try:
        for task in config.tasks:
            task_parser = subparsers.add_parser(task.name, description=task.description)
            for p in task.parameters:
                contribute_parameter(task_parser, p)
            task_parser.set_defaults(task=task)
    except SyntaxError as e:
        parser.error(f"Syntax error in file: {e}")

    return parser, config


def main():
    parser, config = get_parser_and_config()
    args = parser.parse_args()

    if args.list:
        print(" ".join([task.name for task in config.tasks]))
    elif args.validate:
        config.validate_and_exit(level=0)
    elif getattr(args, "task", None):
        args.task.run(args)
    else:
        parser.print_help()
