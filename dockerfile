# Usa uma imagem oficial do Python como base
FROM python:3.11
# Define o diretório de trabalho dentro do container
WORKDIR /app

RUN apt-get update && apt-get install -y make

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Roda o script de inicialização do banco de dados
RUN python src/initialize_db.py

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