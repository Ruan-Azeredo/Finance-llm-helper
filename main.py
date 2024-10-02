import ofxparse
import pandas as pd
import os
from datetime import datetime
from LLMInterface import get_category


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

transaction_with_category = []
for index, transaction in df.iterrows():
    answer = get_category(transaction["Data"].strftime("%d/%m/%Y") + '|' + transaction["Descrição"] + '|' + transaction["Valor"].__str__())
    transaction_with_category.append((transaction, answer))
    print(transaction["Data"], '|', transaction["Descrição"], '|', transaction["Valor"], '|', answer)