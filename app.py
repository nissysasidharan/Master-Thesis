from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Retrieve configuration values from environment variables
db_host = os.getenv("DB_HOST")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Set SQLAlchemy configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}"
)

db = SQLAlchemy(app)



@app.route('/')
def index():
    return render_template('questionaire.html')

@app.route('/cbt')
def cbt():
    return render_template('cbt.html')



if __name__ == '__main__':
    app.run(debug=True)
