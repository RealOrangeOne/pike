#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

set -x

black pike/ tests/ examples/ setup.py pikefile.py
isort pike/ tests/ examples/ setup.py pikefile.py
