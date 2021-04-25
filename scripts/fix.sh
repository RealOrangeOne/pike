#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

set -x

black pike/ tests/ setup.py
isort pike/ tests/ setup.py
