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
