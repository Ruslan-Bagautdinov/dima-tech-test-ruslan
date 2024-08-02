#!/bin/sh

wait_for_db() {
    echo "Waiting for database..."
    while ! nc -z db 5432; do
        sleep 1
    done
    echo "Database is ready!"
}

wait_for_db

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 8000
