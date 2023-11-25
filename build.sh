#!/usr/bin/env bash

set -o errexit
python -m pip install --upgrade pip
poetry install
/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip
python manage.py collectstatic --no-input
python manage.py migrate
