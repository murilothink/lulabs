from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from controllers.user_controller import user_blueprint
from models.models import db
import os

app = Flask(__name__)

ENV = os.getenv("FLASK_ENV", "local")  # Use "docker" no contêiner e "local" fora dele

if ENV == "docker":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/lulabs_db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/lulabs_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialize o db com o app Flask
db.init_app(app)

# Registro do blueprint
app.register_blueprint(user_blueprint)

print("Connecting to database:", app.config['SQLALCHEMY_DATABASE_URI'])

# Criação das tabelas
with app.app_context():
    try:
        print("Creating tables in the database...")
        db.create_all()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)
