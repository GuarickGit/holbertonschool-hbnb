from app import create_app  # ta fonction de création de l'app Flask
from app.extensions import db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database reset done.")
