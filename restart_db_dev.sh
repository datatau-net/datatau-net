#!/usr/bin/env bash
rm app/migrations/000* accounts/migrations/000* db.sqlite3
python manage.py makemigrations dev
python manage.py migrate dev
python manage.py runserver 0.0.0.0:8000 dev
