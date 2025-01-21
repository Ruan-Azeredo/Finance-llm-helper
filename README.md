# Finance LLM Helper
## Descrição
O projeto Finance LLM Helper é um sistema de limpeza de dados de extratos bancários. Ele processa os dados dos extratos, gera tabelas com os gastos mensais e os categoriza automaticamente utilizando um modelo de linguagem (LLM).

## Instalação
Siga os passos abaixo para configurar e executar o projeto corretamente:

### Dependencias para o projeto
- Python
- Docker
- Make

1. .Env
Crie um arquivo .env e adicione as seguintes variáveis:
> Utilize .env.example, no entanto é muito importante lembrar de adicionar a chave de API da GROQ

```bash
GROQ_API_KEY=YOUR_API_KEY

JWT_ACCESS_TOKEN_SECRET= 
JWT_REFRESH_TOKEN_SECRET=
JWT_ALGORITHM=
```

2. **Inicie o Projeto**:

2.1 **Docker**

Execute a imagem da aplicação e a do banco de dados atavez do docker compose:

```bash
docker-compose up
```

A aplicação está pronta!

> Caso esteja desenvolvendo, indicamos executar apenas a imagem do postgres atravez do comando abaixo, e rodar a aplicação atravez dos comandos do *Makefile*

```bash
docker-compose up db -d
```

2.2 **Makefile**

### venv (recomendado)
É recomendado utilizar um ambiente virtual

- No Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

- No Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Rodar app

Este comando abaixo vai:
- Instalar as dependencias
- Iniciar o banco de dados
- Iniciar o servidor

```bash
make build
```

> É importante ter o banco postgres criado e com as credenciais devidamente configuradas, caso não esteja utilizando o docker compose, adicione as variaveis presentes no arquivo *src/database/PostgreSQL.py* no seu .env

Caso queira realizar as ações do `make build` separadamente é possivel também, de uma olhada no Makefile.

## Adicionando Dependências
Se você adicionar uma nova dependência ao projeto, não se esqueça de atualizar o arquivo requirements.txt com o seguinte comando:

```bash
pip freeze > requirements.txt
```

## Testes
O comando `pytest` executa todos os testes do projeto. Incluindo testes que batem na API do LLM ou no DB postgres que podem ser demorados e dependem de dependecias externas.
Para executar os testes excluindo os que são 'llm' e 'db', execute:
```bash
make test
```