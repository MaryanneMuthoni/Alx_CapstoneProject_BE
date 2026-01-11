#!/bin/bash
set -e

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
python3 -m pip install -r requirements.txt

# Apply migrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput
