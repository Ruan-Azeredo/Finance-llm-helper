import pytest
from peewee import PostgresqlDatabase

# Configuração do banco de dados
DATABASE_CONFIG = {
    'database': 'postgres',       # Nome do banco de dados
    'user': 'postgres',           # Usuário do banco
    'password': 'postgres',       # Senha do banco
    'host': '0.0.0.0',          # Host do banco
    'port': 5432,                 # Porta padrão do PostgreSQL
}

@pytest.fixture
def test_db():
    """
    Fixture para criar uma conexão com o banco de dados.
    """
    db = PostgresqlDatabase(
        DATABASE_CONFIG['database'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        host=DATABASE_CONFIG['host'],
        port=DATABASE_CONFIG['port'],
    )
    yield db  # Disponibiliza o banco para os testes
    if not db.is_closed():
        db.close()  # Fecha a conexão após os testes

@pytest.mark.db
def test_database_connection(test_db):
    """
    Testa a conexão com o banco de dados.
    """
    try:
        test_db.connect()
        assert test_db.is_connection_usable()  # Verifica se a conexão é utilizável
        print("Conexão com o banco de dados bem-sucedida!")
    except Exception as e:
        pytest.fail(f"Falha ao conectar ao banco de dados: {e}")
    finally:
        if not test_db.is_closed():
            test_db.close()