#!/bin/bash
set -e
export PATH="/root/.local/bin:$PATH"
cd /var/www/on_courses_backend
git pull origin main
uv sync
uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput
sudo systemctl restart oncourses
