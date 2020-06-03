#!/usr/bin/env bash
./wait-for-it.sh postgresql:5432 -- echo 'postgres is up'
python manage.py init_app
gunicorn -w 2 -b 0.0.0.0:5000 manage:app