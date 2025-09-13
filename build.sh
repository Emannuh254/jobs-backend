#!/usr/bin/env bash
# Install dependencies
pip install -r requirements.txt

# Run Django setup
python manage.py migrate --noinput
python manage.py collectstatic --noinput
