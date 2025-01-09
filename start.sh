#!/bin/bash
set -e

echo "Inicializando o banco de dados..."
python /app/src/verifyDbConnection.py

echo "Iniciando o servidor FastAPI..."
exec "$@"