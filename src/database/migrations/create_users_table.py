from database import db
from models import User

def create_users_table():
    db.connect()
    db.create_tables([User])

    print('Tabela users criada com sucesso!')