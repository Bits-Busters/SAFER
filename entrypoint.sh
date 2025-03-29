#!/bin/sh

# Sai imediatamente se um comando falhar
set -e

# Aplica as migrações
python3 Projeto/manage.py makemigrations SAFERapp
python3 Projeto/manage.py migrate



# Inicia o Gunicorn
exec gunicorn --bind 0.0.0.0:8000 Projeto.asgi:application -c gunicorn.conf.py