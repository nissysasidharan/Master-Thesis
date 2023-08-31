from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
import secrets
from database  import db, init_db, Users
import bcrypt


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Generate a secure secret key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

# Retrieve configuration values from environment variables
db_host = os.getenv("DB_HOST")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Set SQLAlchemy configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}"
)


# Initialize the SQLAlchemy instance with the Flask app
init_db(app)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        # Log the user in
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('home'))


@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists.', 'error')
        return redirect('home.html')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = Users(username=username, password_hash=hashed_password, email=email)


    db.session.add(new_user)
    db.session.commit()

    flash('User created successfully! You can now log in.', 'success')
    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



if __name__ == '__main__':
    app.run(debug=True)