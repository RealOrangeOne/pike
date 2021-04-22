import argparse
import copy
from pathlib import Path
from typing import List, Optional

from pike.utils import noop

DEFAULT_FILE_NAME = "pikefile.py"


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

    args = parser.parse_args(args=argv)
    args.file = file  # Poke the file back in
    return args


def main():
    args = get_args()
    print("Got args", args)


if __name__ == "__main__":
    main()
