from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

connection = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    autocommit=True,
    ssl_ca="/etc/ssl/cert.pem",  # Use the correct path to your SSL CA certificate
    ssl_verify_identity=True
)



app = Flask(__name__)
@app.route('/')
def index():
    return render_template('questionaire.html')



if __name__ == '__main__':
    app.run(debug=True)
