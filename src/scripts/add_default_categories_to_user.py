from database import db
from models import Category

db.connect()

Category.create_default_categories(3)

db.close()