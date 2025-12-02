#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install all dependencies
pip install -r requirements.txt

# 🔥 Delete old staticfiles before collecting
rm -rf staticfiles

# Run migrations (optional but recommended)
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput
