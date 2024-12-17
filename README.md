# Finance LLM Helper
## Descrição
O projeto Finance LLM Helper é um sistema de limpeza de dados de extratos bancários. Ele processa os dados dos extratos, gera tabelas com os gastos mensais e os categoriza automaticamente utilizando um modelo de linguagem (LLM).

## Instalação
Siga os passos abaixo para configurar e executar o projeto corretamente:

1. **Crie um ambiente virtual** (recomendado):

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

2. **Inicie o Projeto**:

Este comando abaixo vai:
- Instalar as dependencias
- Criar o banco de dados
- Iniciar o servidor

```bash
make build
```

Caso queira realizar as ações do `make build` separadamente é possivel também, de uma olhada no Makefile.

## Adicionando Dependências
Se você adicionar uma nova dependência ao projeto, não se esqueça de atualizar o arquivo requirements.txt com o seguinte comando:

```bash
pip freeze > requirements.txt
```
## Crie .Env
Crie um arquivo .env e adicione as seguintes variáveis:

```bash
GROQ_API_KEY=YOUR_API_KEY

JWT_ACCESS_TOKEN_SECRET= 
JWT_REFRESH_TOKEN_SECRET=
JWT_ALGORITHM=
```


## Testes
O comando `pytest` executa todos os testes do projeto. Incluind testes que batem na API do LLM que podem ser demorados e dependem de dependecias externas.
Para executar os testes excluindo os que são 'llm', execute:
```bash
    make test
```

## To do

- [x] Melhorar arquitetura (adicionado ./src)
- [x] Criar class para file
- [x] Maior cobertura de gerenciamento de erros
- [x] Implementar testes unitarios e de integração
- [x] Realocar defs da main
- [x] Flexibilizar leitura de .csv de acordo com padrões de outros bancos
- [x] Transformar em api
- [x] Fazer testes de integração com o LLM
- [ ] Garantir que o id de cada transação seja unico
- [x] Adicionar DB
- [x] Criar contas p/ cada usuario
- [ ] Salvar as transações