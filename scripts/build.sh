#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

set -x

rm -rf *.egg-info build/ dist/

python setup.py clean

python -m build --sdist --wheel .
