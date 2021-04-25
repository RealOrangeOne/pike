#!/usr/bin/env bash

set -e

PATH=env/bin:${PATH}

set -x

pytest --verbose --cov pike/ --cov-report term --cov-report html tests/

black --check pike/ tests/ setup.py
flake8 pike/ tests/ setup.py
isort --check pike/ tests/ setup.py
mypy pike/ tests/ setup.py
