from peewee import PostgresqlDatabase
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

"""
O host pode causar certo problema, pois quando rodamos a apicação e o banco de dados atraves do docker-compose, ambos estão na mesma rede, então o host é o nome do serviço do banco de dados, que no caso é "db", já quando rodamos apenas o banco de dados, o host é "localhost", pois o banco de dados está rodando na máquina local.
Para solucionar isto quando a apllicação atraves o makefile, foi criado uma variável de ambiente chamada "POSTGRES_HOST" que é setada no arquivo .env, e é utilizada para definir o host do banco de dados como locahost.
"""

db = PostgresqlDatabase(
    POSTGRES_DB or "postgres",
    user = POSTGRES_USER or "postgres",
    password = POSTGRES_PASSWORD or "postgres",
    host = POSTGRES_HOST or "db",
    port = 5432
)