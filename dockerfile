# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Roda o script de inicialização do banco de dados
RUN python src/initialize_db.py

# Exponha a porta que o FastAPI usará
EXPOSE 8000

# Comando para iniciar o servidor FastAPI
CMD ["cd", "src", "&&", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

# --------------------------------------------

# Criar imagem
# docker build -t spendlyzer .

# Rodar imagem
# docker run -p 8000:8000 spendlyzer


# Esta imagem gerada não está rodando corretamente, precisa ser fixada posteriormente