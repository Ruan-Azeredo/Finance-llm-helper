from peewee import Model
from playhouse.migrate import SqliteMigrator, migrate
from playhouse.reflection import Introspector
from pathlib import Path

from models import User
from database import db

def initialize_db():

    # Muito importante adicionar os modelos aqui
    models = [User]

    if not Path('database.db').exists():
        db.connect()
        db.create_tables(models)

        print('Banco de dados criado com sucesso!')
    else:
        db.connect()
        
        if db.is_connection_usable():
            print('Banco de dados ja existe!')


            for model in models:
                update_database(model = model)

def update_database(model: Model):

    print('Verificando banco de dados...')

    table_name = model._meta.table_name

    try:
        # Cria o introspector para inspecionar o banco
        introspector = Introspector.from_database(db)
        
        # Obter informações sobre as tabelas no banco
        database_schema = introspector.generate_models()

        # Verifica se a tabela existe no banco
        if table_name not in database_schema:
            raise ValueError(f"A tabela '{table_name}' não foi encontrada no banco de dados.")
        
        # Recupera o modelo da tabela
        table_model = database_schema[table_name]
        table_columns = table_model._meta.fields

        # Recupera as colunas do modelo
        model_columns = model._meta.fields

        for column_name in table_columns:
            if column_name not in model_columns:
                print(f"Campo '{column_name}' está presente na TABELA, mas ausente no MODELO.")

                make_change: bool = input("Deseja remover este campo da tabela? (S = enter /N = n): ").lower() == ""
                if make_change:
                    try:
                        migrate(
                            SqliteMigrator(db).drop_column(table_name, column_name, table_columns[column_name])
                        )
                        print('Operaçao concluida com sucesso')
                    except Exception as e:
                        print(f"Erro ao remover campo da tabela: {e}")
        
        # Verifica colunas no modelo que estão ausentes no banco
        for column_name in model_columns:
            if column_name not in table_columns:
                print(f"Campo '{column_name}' está presente no MODELO, mas ausente na TABELA.")

                make_change: bool = input("Deseja adicionar este campo a tabela? (S = enter /N = n): ").lower() == ""
                if make_change:
                    try:
                        migrate(
                            SqliteMigrator(db).add_column(table_name, column_name, model_columns[column_name])
                        )
                        print('Operaçao concluida com sucesso')
                    except Exception as e:
                        print(f"Erro ao adicionar campo da tabela: {e}")

        # Verifica diferenças em tipos de campo ou nullabilidade
        for column_name in table_columns:
            if column_name in model_columns:
                table_field = table_columns[column_name]
                model_field = model_columns[column_name]

                if table_field.field_type != model_field.field_type:
                    print(f"Campo '{column_name}' tem tipos diferentes: "
                          f"TABELA({table_field.field_type}) vs MODELO({model_field.field_type})")
                    
                    print('\nPor limitações do sqlite, nao e possivel alterar o tipo de campo.')

                rows_atributes = ['null', 'unique', 'default', 'primary_key']

                for atribute in rows_atributes:

                    table_field_value = getattr(table_field, atribute)
                    model_field_value = getattr(model_field, atribute)

                    if table_field_value != model_field_value:
                        print(f"\nCampo '{column_name}' tem o atributo {atribute} diferente: \n"
                            f"TABELA({atribute}={table_field_value}) vs MODELO({atribute}={model_field_value})")
                        
                        print('\nPor limitações do sqlite, nao e possivel realizar alterações nos atributos das colunas.')

        print("\nComparação concluída.")
    except Exception as e:
        print(f"Erro ao sincronizar o banco de dados: {e}")

if __name__ == '__main__':
    initialize_db()