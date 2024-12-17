from peewee import CharField
from playhouse.migrate import migrate, SqliteMigrator

from database import db

with db.atomic():
    try:
        migrate(
            SqliteMigrator(db).add_column('users', 'role', CharField(default = "free"))
        )
        print("Coluna role criada em 'users' com sucesso!")
    except:
        print("Ocorreu um erro, confira o banco de dados.")