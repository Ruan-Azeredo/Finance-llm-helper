from peewee import PostgresqlDatabase
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

db = PostgresqlDatabase(
    POSTGRES_DB or "postgres",
    user = POSTGRES_USER or "postgres",
    password = POSTGRES_PASSWORD or "postgres",
    host = POSTGRES_HOST or "db",
    port = 5432
)