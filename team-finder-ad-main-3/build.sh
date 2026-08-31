#!/usr/bin/env bash
# Скрипт сборки для Render. Устанавливает зависимости,
# собирает статику и применяет миграции при каждом деплое.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
