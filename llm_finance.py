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
                    'date': transaction.date,
                    'payee': transaction.payee,
                    'amount': transaction.amount,
                    'id': transaction.id,
                })

        df_temp = pd.DataFrame(transsactions_data)
        df_temp['amount'] = df_temp['amount'].astype(float)