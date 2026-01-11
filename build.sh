#!/usr/bin/env bash
set -o errexit

# Install dependencies
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Apply migrations
python3 student_records/manage.py migrate

# Collect static files
python3 student_records/manage.py collectstatic --noinput

