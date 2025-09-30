from database import db
from models import User, Transaction, Account

import math

"""
Para realizar alteraçõs no banco de dados que envolvam certa lógica, é necessário criar um script.
Siga o exemplo estrutural abaixo.
"""

db.connect()

# ----------------Logica acessando data----------------------

try:
    users = User.all()

    for user in users:
        account = Account.create(user_id=user.id, name='Minha Conta')
        user.update(default_account_id=account.id)

        transactions_user_list = Transaction.get_transactions_by_user_id(user.id, 0, 100_000_000_000)
        print(transactions_user_list)
        for transaction in transactions_user_list:
            print(transaction)
            transaction.update(account_id=account.id)

    print('All users now have default account\nThe user have deafult_account_id setted\nThe transactions have the releated account_id')
except Exception as e:
    print("Error: ", e)
    db.rollback()

db.close()