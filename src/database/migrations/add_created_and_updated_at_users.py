from peewee import IntegerField
from playhouse.migrate import migrate, SqliteMigrator

from database import db

"""
Para adicionar mais colunas no banco de dados:

with db.atomic():
    migrate(
        * coluna *
    )

É importante adicionar o campo no respectivo model.

Rode o respectivo script (este arquivo por exemplo) para criar as colunas no banco de dados.

"""

with db.atomic():
    migrate(
        SqliteMigrator(db).add_column('user', 'created_at', IntegerField(null = True)),
    )

with db.atomic():
    migrate(
        SqliteMigrator(db).add_column('user', 'updated_at', IntegerField(null = True)),
    )