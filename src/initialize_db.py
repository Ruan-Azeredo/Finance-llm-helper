from pathlib import Path
from peewee import SqliteDatabase

from models import User
from database import db

def initialize_db():
    if not Path('database.db').exists():
        db.connect()
        db.create_tables([User])

        print('Banco de dados criado com sucesso!')
    else:
        print('Banco de dados ja existe!')

if __name__ == '__main__':
    initialize_db()