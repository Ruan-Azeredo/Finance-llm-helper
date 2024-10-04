import ofxparse
import os
from datetime import datetime
from LLMInterface import get_category

from models.transaction import Transaction

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

def get_transaction_description(transaction: Transaction):
    return transaction.format_description_transaction()

df = []

for file in os.listdir('extratos'):
    ofx = get_ofx_from_file(file)
    transactions_data = get_transaction_data(ofx)
    for transaction_in_data in transactions_data:
        transaction = Transaction(
            transaction_in_data["id"],
            transaction_in_data["Data"],
            transaction_in_data["Valor"],
            transaction_in_data["Descrição"]
        )

        df_temp = transaction.treatment_data()
        df.append(df_temp)

transaction_with_category = []
for transaction in df:
    description = get_transaction_description(transaction)
    answer = get_category(description)
    transaction_with_category.append((transaction, answer))
    print(transaction.date, '|', transaction.description, '|', transaction.value, '|', answer)