from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

connection = MySQLdb.connect(
  host= os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd= os.getenv("DB_PASSWORD"),
  db= os.getenv("DB_NAME"),
  autocommit = True,
  ssl_mode = "VERIFY_IDENTITY",
  ssl_ca="/Users/nissysasidharan/ca.pem",
  ssl_cert="/Users/nissysasidharan/server-cert.pem",
  ssl_key="/Users/nissysasidharan/server-key.pem"
)


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('questionaire.html')



if __name__ == '__main__':
    app.run(debug=True)
