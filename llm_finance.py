import ofxparse
import pandas as pd
import os
from datetime import datetime


df = pd.DataFrame()

for file in os.listdir('extratos'):
    with open(f'extratos/{file}', encoding='ISO-8859-1') as ofx_file:
        ofx = ofxparse.OfxParser.parse(ofx_file)

        transsactions_data = []

        for account in ofx.accounts:
            for transaction in account.statement.transactions:
                transsactions_data.append({
                    'Data': transaction.date,
                    'Descrição': transaction.memo,
                    'Valor': transaction.amount,
                    'id': transaction.id,
                })

        df_temp = pd.DataFrame(transsactions_data)
        df_temp['Valor'] = df_temp['Valor'].astype(float)
        df_temp['Data'] = df_temp['Data'].apply(lambda x: x.date())
        df = pd.concat([df, df_temp])

#### LLM

from langchain_openai import ChatOpenAI
from  langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_  = load_dotenv(find_dotenv())

template = """
Você é um analista de dados, trabalhando em um projeto de dados.
Seu trabalho é escolher uma categoria adequada para cada transação financeira que vou lhe enviar.
Todas são transações financeiras de uma pessoa física.

Escoha uma dentre as seguintes categorias:
- Alimentação
- Receitas
- Saúde
- Transporte
- Mercado
- Educação
- Compras
- Investimento
- Transferencia para terceiros
- Telefone
- Moradia

Escolha a categoria deste item:
{text}

Responsa apenas com a categoria.
"""

prompt = PromptTemplate.from_template(template=template)
chat = ChatGroq(model="llama-3.1-8b-instant")
chain = prompt | chat

category = []
for transaction in list(df["Descrição"].values):
    awsn = chain.invoke(transaction).content
    category.append(awsn)