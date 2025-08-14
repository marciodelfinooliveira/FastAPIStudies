#!/bin/sh

# Garante que o script pare se algum comando falhar
set -e

# Espera o PostgreSQL iniciar completamente
echo "Waiting for PostgreSQL to start..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL started"

# Aplica as migrações do banco de dados
# 'alembic upgrade head' aplica todas as migrações pendentes.
echo "Applying database migrations..."
alembic upgrade head

# Inicia a aplicação FastAPI com Uvicorn
echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
