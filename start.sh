#!/bin/bash
set -e
sleep 2
echo "Inicializando o banco de dados..."
python /app/src/verifyDbConnection.py

echo "Iniciando o servidor FastAPI..."
exec "$@"