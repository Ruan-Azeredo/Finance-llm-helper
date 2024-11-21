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

2. **Instale as dependências**: Após ativar o ambiente virtual, instale as dependências listadas no arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

3. **Adicione os extratos**: Adicione extratos  no formato .ofx em uma pasta /extratos no diretorio do projeto.

4. **Execute o projeto**: Após a instalação, você poderá rodar os scripts disponíveis no projeto, como o `llm_finance.py`.

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
O comando `pytest` executa todos os testes do projeto. Incluind testes e2e que podem ser demorados e dependem de dependecias externas.
Para executar os testes excluindo os que são e2e, execute:
```bash
    pytest -m "not e2e"
```

Para executar os testes e2e, execute:
```bash
    pytest -m e2e
```

##### O mesmo vale para a tag `llm`, que é ainda mais delicada de ser testada por dependencias externas  mais fortes.

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
- [ ] Adicionar DB
- [ ] Criar contas p/ cada usuario
- [ ] Salvar as transações