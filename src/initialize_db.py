from models import User, Category
from dotenv import load_dotenv
from database import db
import os

# Criar um novo usuário
def create_user(name, email, password, role='free'):
    try:
        user = User.create(
            name=name,
            email=email,
            password=password,
            role=role
        )
        Category.create_default_categories(user.id)
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        
    print(f"Usuário criado: {user.name} (ID: {user.id})")

# Exemplo de uso
if __name__ == '__main__':

    load_dotenv()

    USER_DEFAULT_EMAIL= os.getenv("USER_DEFAULT_EMAIL")
    USER_DEFAULT_PASS= os.getenv("USER_DEFAULT_PASS")
    create_user(
        name='Joe Doe',
        email=USER_DEFAULT_EMAIL,
        password=USER_DEFAULT_PASS  # Você pode usar um hash aqui em um sistema real
    )