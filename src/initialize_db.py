from peewee import Model
from playhouse.migrate import PostgresqlDatabase, migrate
from playhouse.reflection import Introspector
from pathlib import Path
from typing import Any

from models import models
from database import db

migrator = PostgresqlDatabase(db)

def initialize_db() -> None:

    try:
        db.connect()
        print("Conexão com o banco de dados bem-sucedida!")

        for model in models:
            if not db.table_exists(model._meta.table_name):
                print(f"Criando tabelas para o modelo: {model.__name__}")
                db.create_tables([model])
            else:
                print(f"Tabela do modelo {model.__name__} já existe. Checkando atualizações...")
                update_database(model)

        print("Setup do banco de dados concluído com sucesso!")

    except Exception as e:
        print(f"Erro ao conectar ao banco ou na geração/atualização de tabelas: {e}")

    finally:
        if not db.is_closed():
            db.close()
            print("Conexão com o banco de dados terminada.")

def _handle_table_model(model: Model) -> tuple[str, dict[str, Any]]:

    try:
        table_name = model._meta.table_name

        # Cria o introspector para inspecionar o banco
        introspector = Introspector.from_database(db)
        
        # Obter informações sobre as tabelas no banco
        database_schema = introspector.generate_models()

        # Verifica se a tabela existe no banco
        if table_name not in database_schema:
            print(f"A tabela '{table_name}' não foi encontrada. Criando a tabela...")
            with db:
                db.create_tables([model])  # Cria a tabela associada ao modelo
            print(f"Tabela '{table_name}' criada com sucesso.")

        # Atualiza o schema após criação (caso necessário)
        database_schema = introspector.generate_models()
        
        # Recupera o modelo da tabela
        table_model = database_schema[table_name]
        table_columns = table_model._meta.fields

        return table_name, table_columns
        
    except Exception as error:
        raise Exception(f"Erro ao acessar modelo da tabela {table_name}: {error}")
    
def _verify_table_missing_columns(model_columns: dict[str, Any], table_columns: dict[str, Any], table_name: str) -> None:
    for column_name in table_columns:
        if column_name not in model_columns:
            print(f"Campo '{column_name}' está presente na TABELA, mas ausente no MODELO.")

            make_change: bool = input("Deseja remover este campo da tabela? (S = enter /N = n): ").lower() == ""
            if make_change:
                try:
                    migrate(
                        migrator.drop_column(table_name, column_name, table_columns[column_name])
                    )
                    print('Operaçao concluida com sucesso')
                except Exception as e:
                    print(f"Erro ao remover campo da tabela: {e}")

def _verify_table_leftover_columns(model_columns: dict[str, Any], table_columns: dict[str, Any], table_name: str) -> None:
    for column_name in model_columns:
        if column_name not in table_columns:
            print(f"Campo '{column_name}' está presente no MODELO, mas ausente na TABELA.")

            make_change: bool = input("Deseja adicionar este campo a tabela? (S = enter /N = n): ").lower() == ""
            if make_change:
                try:
                    migrate(
                        migrator.add_column(table_name, column_name, model_columns[column_name])
                    )
                    print('Operaçao concluida com sucesso')
                except Exception as e:
                    print(f"Erro ao adicionar campo da tabela: {e}")

def _verify_fields_type_and_attributes(model_columns: dict[str, Any], table_columns: dict[str, Any], table_name: str) -> None:
    for column_name in table_columns:
        if column_name in model_columns:
            table_field = table_columns[column_name]
            model_field = model_columns[column_name]

            if table_field.field_type != model_field.field_type:
                print(f"\nCampo '{column_name}' tem tipos diferentes: "
                        f"TABELA({table_field.field_type}) vs MODELO({model_field.field_type})")
                
                print('\nPor limitações do sqlite, nao e possivel alterar o tipo de campo.')

            rows_atributes = [
                'null',
                #'unique', # O SQLite nao suporta este atrbuto na tabela, como o modelo garante o correto funcionamento nao é preciso se preocupar.
                #'default', # O SQLite nao suporta este atrbuto na tabela, como o modelo garante o correto funcionamento nao é preciso se preocupar.
                'primary_key'
            ]

            for atribute in rows_atributes:

                table_field_value = getattr(table_field, atribute)
                model_field_value = getattr(model_field, atribute)

                if table_field_value != model_field_value:
                    print(f"\nCampo '{column_name}' tem o atributo {atribute} diferente: "
                        f"TABELA({atribute}={table_field_value}) vs MODELO({atribute}={model_field_value})")
                    
                    print('\nPor limitações do sqlite, nao e possivel realizar alterações nos atributos das colunas.')

def update_database(model: Model) -> None:

    print('Verificando banco de dados...')

    try:
        table_name, table_columns = _handle_table_model(model)

        # Recupera as colunas do modelo
        model_columns = model._meta.fields

        _verify_table_missing_columns(model_columns, table_columns, table_name)
        
        _verify_table_leftover_columns(model_columns, table_columns, table_name)

        _verify_fields_type_and_attributes(model_columns, table_columns, table_name)

        print("\nComparação concluída.")
    except Exception as e:
        print(f"Erro ao sincronizar o banco de dados: {e}")

if __name__ == '__main__':
    initialize_db()