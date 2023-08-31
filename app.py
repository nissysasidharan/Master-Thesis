from flask import Flask, render_template, request, redirect

from dotenv import load_dotenv
import os
import MySQLdb

# Load environment variables from .env
load_dotenv()

# Create a MySQL connection
connection = MySQLdb.connect(
  host= os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd= os.getenv("DB_PASSWORD"),
  db= os.getenv("DB_NAME"),
  autocommit = True,
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ssl_ca": "/etc/ssl/cert.pem"
  }
)


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('questionaire.html')

def cbt():
    return render_template('cbt.html')



if __name__ == '__main__':
    app.run(debug=True)
