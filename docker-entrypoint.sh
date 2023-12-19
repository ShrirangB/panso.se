#!/bin/sh

# Exit on error
set -e

# Debug
set -x

# Wait for database
echo "Waiting for database"
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
done
echo "Database started"

# Wait for redis
echo "Waiting for redis"
while ! nc -z "$REDIS_HOST" 6379; do
  sleep 0.1
done
echo "Redis started"

# Django entrypoint script
# 1. Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput
echo "Collect static files done"

# 2. Apply database migrations
echo "Apply database migrations"
python manage.py migrate
echo "Apply database migrations done"

# 3. Start server
echo "Starting server"
gunicorn --workers=9 --bind=0.0.0.0:8000 panso.wsgi:application --log-level=info --access-logfile=- --error-logfile=-
echo "Bye"
