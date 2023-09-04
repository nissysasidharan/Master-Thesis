from flask import Flask, render_template, redirect, session, request, flash
import mysql.connector
import secrets
from config import DATABASE_CONFIG
from database import RecommendedArticle, RecommendedVideo, RecommendedBook, RecommendedPodcast, Users

app = Flask(__name__)

# Create a database connection
db_connection = mysql.connector.connect(**DATABASE_CONFIG)
db_cursor = db_connection.cursor()

# Generate a secure secret key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key


@app.route('/')
def index():
    return render_template('home.html')

def create_user(username, email, password):
    try:
        # Assuming you have a Users table with columns: username, email, password
        query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, password)
        db_cursor.execute(query, values)
        db_connection.commit()
        return True  # User created successfully
    except Exception as error:
        print(f"Error creating user: {error}")
        return False  # Error creating user

@app.route("/create_user", methods=["GET", "POST"])
def create_user_route():
    if request.method == "POST":
        # Handle the form submission for creating a user
        # Extract the form data and insert it into the database
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Call the function to create the user in the database (using database.py)
        if create_user(username, email, password):
            # If user creation is successful, redirect to the dashboard
            session['username'] = username
            return redirect('/dashboard')
        else:
            # If user creation fails, show an error message
            flash("Error creating user")

    return render_template("home.html")
@app.route('/dashboard')
def dashboard():
    if "username" in session:
        username = session["username"]
        return render_template("dashboard.html", username=username)
    else:
        return redirect("/")

#Main Execution
if __name__ == "__main__":
    app.run(port=5001)
