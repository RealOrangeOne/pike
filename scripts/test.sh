#!/usr/bin/env bash

set -e

PATH=env/bin:${PATH}

set -x

pytest --verbose --cov pike/ --cov-report term --cov-report html tests/

black --check pike/ tests/ examples/ setup.py pikefile.py
flake8 pike/ tests/ examples/ setup.py pikefile.py
isort --check pike/ tests/ examples/ setup.py pikefile.py

mypy pike/ tests/ setup.py pikefile.py
mypy examples/
