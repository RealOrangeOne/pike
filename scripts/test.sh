#!/usr/bin/env bash

set -e

PATH=env/bin:${PATH}

set -x

black --check pike/ setup.py
flake8 pike/ setup.py
isort --check pike/ setup.py
mypy pike/ setup.py
