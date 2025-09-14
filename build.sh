#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
# This command gathers all your CSS, JS, and image files into one place for the server.
python manage.py collectstatic --no-input

# Apply database migrations
# This command creates the necessary tables in your database (like for users, plans, etc.).
python manage.py migrate

# Create a superuser (admin user) automatically if it doesn't already exist.
# It uses the environment variables you set on Render.
# IMPORTANT: This command will only create the user the first time it's run.
# If a user with the same username already exists, it will do nothing.
python manage.py createsuperuser --no-input
