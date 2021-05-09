from pathlib import Path

import pytest

from pike import DEFAULT_FILE_NAME

ROOT = Path(__file__).parents[1]


@pytest.fixture
def example_pikefile() -> Path:
    return ROOT / "examples" / DEFAULT_FILE_NAME


@pytest.fixture
def root() -> Path:
    return ROOT
