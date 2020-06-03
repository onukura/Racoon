#!/usr/bin/env bash
./wait-for-it.sh postgresql:5432 -- echo 'postgres is up'
python manage.py init_app
waitress-serve --listen=0.0.0.0:5000 manage:app