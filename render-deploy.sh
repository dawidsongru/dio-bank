#!/usr/bin/env bash
set -e

poetry run flask --app app db upgrade
poetry run gunicorn wsgi:app