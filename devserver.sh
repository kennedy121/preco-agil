#!/bin/sh
source .venv/bin/activate
# Usamos 'run' como app, e definimos a porta 8000 como padrão caso $PORT não exista.
python -u -m flask --app run run --host=0.0.0.0 --port=${PORT:-8000} --debug
