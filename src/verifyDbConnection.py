from database import db

def verifyDbConnection():
    try:
        db.connect()
        print("Conexão com o banco de dados bem-sucedida!")
        tables = db.get_tables()
        print(f"Tabelas: {tables}")
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")

if __name__ == '__main__':
    verifyDbConnection()