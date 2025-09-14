#!/usr/bin/env bash
# This script runs the necessary commands to build the Django application on Render.

# Exit immediately if a command exits with a non-zero status.
set -o errexit

# Install all Python dependencies from requirements.txt
echo "--- Installing dependencies ---"
pip install -r requirements.txt

# Collect all static files (CSS, JS, etc.) into a single directory
echo "--- Collecting static files ---"
python manage.py collectstatic --no-input

# Run our custom management command to apply migrations and create a superuser
echo "--- Running production setup (migrations & superuser) ---"
python manage.py setup_production

echo "--- Build finished successfully! ---"
