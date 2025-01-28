from database import db
from models import User

"""
Para realizar alteraçõs no banco de dados que envolvam certa lógica, é necessário criar um script.
Siga o exemplo estrutural abaixo.
"""

db.connect()

# ----------------Logica acessando data----------------------

try:
    users = User.all()

    for user in users:
        if user.email and not user.email.endswith('.br'):
            user.email = user.email + '.br'
            user.save()
except Exception as e:
    print(e)
    db.rollback()

# ----------------------Resposta no terminal------------------
print('All users\' emails were updated to .br')

# ------------------------------------------------------------

db.close()