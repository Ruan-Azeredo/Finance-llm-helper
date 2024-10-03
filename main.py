import ofxparse
import pandas as pd
import os
from datetime import datetime
from LLMInterface import get_category

def get_ofx_from_file(file):
    with open(f'extratos/{file}', encoding='ISO-8859-1') as ofx_file:
        return ofxparse.OfxParser.parse(ofx_file)
    
def get_transaction_data(ofx):
    transactions_data = []

    for account in ofx.accounts:
        for transaction in account.statement.transactions:
            transactions_data.append({
                'Data': transaction.date,
                'Descrição': transaction.memo,
                'Valor': transaction.amount,
                'id': transaction.id,
            })

    return transactions_data

def treatment_data(transactions_data):
    df = pd.DataFrame(transactions_data)
    df['Valor'] = df['Valor'].astype(float)
    df['Data'] = df['Data'].apply(lambda x: x.date())
    return df

def format_description_transaction(transaction):
    return transaction["Data"].strftime("%d/%m/%Y") + '|' + transaction["Descrição"] + '|' + transaction["Valor"].__str__()

df = pd.DataFrame()

for file in os.listdir('extratos'):
    ofx = get_ofx_from_file(file)
    transactions_data = get_transaction_data(ofx)

    df_temp = treatment_data(transactions_data)
    df = pd.concat([df, df_temp])

transaction_with_category = []
for index, transaction in df.iterrows():
    description = format_description_transaction(transaction)
    answer = get_category(description)
    transaction_with_category.append((transaction, answer))
    print(transaction["Data"], '|', transaction["Descrição"], '|', transaction["Valor"], '|', answer)