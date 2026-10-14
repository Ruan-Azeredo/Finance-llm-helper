# Usa uma imagem oficial slim do Python para reduzir drasticamente o consumo de memória e disco
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Variáveis de ambiente para otimização de runtime e instalação
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instala curl para checagens de integridade e limpa o cache do apt para economizar espaço
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala apenas os requirements de produção primeiro (aproveitamento ótimo de cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Define o diretório de trabalho para o código da aplicação
WORKDIR /app/src

# Exponha a porta que o FastAPI usará
EXPOSE 8000

# Cria um script de inicialização para rodar o `verifyDbConnection.py` antes do servidor
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Usa o script de inicialização como ponto de entrada
ENTRYPOINT ["/start.sh"]

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

# --------------------------------------------

# Criar imagem
# docker build -t spendlyzer .

# Rodar imagem
# docker run -p 8000:8000 spendlyzer