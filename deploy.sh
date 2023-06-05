#!/bin/bash

# Upgrade pip
pip install --upgrade pip

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi
