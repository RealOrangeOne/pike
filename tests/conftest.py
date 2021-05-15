from pathlib import Path

import pytest

from pike.cli.config import PikeFile

ROOT = Path(__file__).parents[1]


@pytest.fixture
def example_pikefile_path() -> Path:
    return ROOT / "examples" / PikeFile.DEFAULT_FILE_NAME


@pytest.fixture
def root() -> Path:
    return ROOT
