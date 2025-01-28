from database import db

db.connect()

query = "SELECT * FROM users;"
users = db.execute_sql(query)

for user in users:
    print(user)

db.close()