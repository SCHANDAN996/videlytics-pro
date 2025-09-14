#!/usr/bin/env bash
# Exit on error, ensuring that the script will stop if any command fails.
set -o errexit

echo "Starting build process..."

# Step 1: Install all dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Step 2: Collect all static files (CSS, JS, images)
# The --no-input flag prevents the command from asking for confirmation.
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Step 3: Apply database migrations
# This is the most crucial step. It creates all the necessary tables in the database.
echo "Applying database migrations..."
python manage.py migrate

# Step 4: Create a superuser (admin) only if it doesn't already exist.
# This part is now handled by a separate Django management command for reliability.
# We will create this command in the next step.
# For now, we will use the same logic as before.
echo "Creating superuser..."
python manage.py createsuperuser --no-input || echo "Superuser already exists."

echo "Build process finished successfully!"
