import os
import shlex
from subprocess import run

TEST_FILES = [
    "pike/",
    "tests/",
    "examples/",
    "setup.py",
    "pikefile.py",
]


def _run_in_venv(cmd):
    return run(cmd, env={"PATH": f"env/bin:{os.environ['PATH']}"}, check=True)


def test():
    """
    Run the test suite
    """
    for cmd in [
        "pytest --verbose --cov pike/ --cov-report term --cov-report html tests/",
    ]:
        _run_in_venv(shlex.split(cmd))
    for linter in [["black", "--check"], ["flake8"], ["isort", "--check"]]:
        _run_in_venv(linter + TEST_FILES)

    _run_in_venv(
        ["mypy", "pike/", "tests/", "setup.py", "pikefile.py", "--show-error-codes"]
    )
    _run_in_venv(["mypy", "examples/"])
    _run_in_venv(["bandit", "-r", "pike/"])


def fix():
    """
    Run the lint fixers for `black` and `isort`
    """
    _run_in_venv(["black"] + TEST_FILES)
    _run_in_venv(["isort"] + TEST_FILES)


def build():
    run(["./scripts/build.sh"])
