from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create instances of Flask-SQLAlchemy and Flask-Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

# Define your database models here using SQLAlchemy
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Add any other models you need here

# Define functions to interact with the database
def create_user(username, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = Users(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

# Add other database-related functions as needed

# Initialize the database with the Flask app
def init_db(app):
    db.init_app(app)
