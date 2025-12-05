#!/bin/bash
set -e

echo "=========================================="
echo "E-CMS Docker Entrypoint"
echo "=========================================="

# Wait for database to be ready
if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 1
    done
    echo "PostgreSQL is ready!"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_cms.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'admin123')
    print('Superuser created: admin@example.com / admin123')
else:
    print('Superuser already exists')
"

echo "=========================================="
echo "Starting application..."
echo "=========================================="

# Execute the main command
exec "$@"
