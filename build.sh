#!/usr/bin/env bash
# This script runs the necessary commands to build the Django application on Render.

# Exit immediately if a command exits with a non-zero status.
set -o errexit

echo "--- Installing dependencies ---"
pip install -r requirements.txt

# The --clear flag is important to remove old static files
echo "--- Collecting static files ---"
python manage.py collectstatic --no-input --clear

# This is the most important command. It will now use the migration files.
echo "--- Applying database migrations ---"
python manage.py migrate

# Create a superuser if it doesn't exist, using environment variables
echo "--- Creating superuser ---"
python manage.py createsuperuser --no-input || echo "Superuser already exists."

echo "--- Build finished successfully! ---"

