#!/bin/bash
echo "=== Starting CareerConnect Build for Vercel ==="

# Install Python requirements
python3 -m pip install -r requirements.txt

# Run migrations if database is configured
python3 manage.py migrate --noinput || echo "Database migration skipped or deferred to external DB."

# Collect static files into staticfiles/
python3 manage.py collectstatic --noinput --clear

echo "=== Vercel Build Completed Successfully ==="
