#Imports and Setup

from flask import Flask, render_template, redirect, session, request, flash
#import mysql.connector
import secrets
from config import DATABASE_CONFIG
from database import RecommendedArticle, RecommendedVideo, RecommendedBook, RecommendedPodcast, Users

app = Flask(__name__)

#Create a database connection
db_connection = mysql.connector.connect(**DATABASE_CONFIG)
db_cursor = db_connection.cursor()

# Generate a secure secret key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

#Routes
@app.route('/')
def index():
    return render_template('home.html')

def create_user(username, email, password):
    try:
        new_user = Users(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

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

@app.route('/recommendation.html')
def recommended_articles():
   # db_cursor.execute("SELECT * FROM recommended_articles")
    #recommended_articles_data = db_cursor.fetchall()

    #db_cursor.execute("SELECT * FROM recommended_videos")
   # recommended_videos_data = db_cursor.fetchall()

    #db_cursor.execute("SELECT title,link FROM recommended_books")
    #recommended_books_data = db_cursor.fetchall()

    #db_cursor.execute("SELECT * FROM recommended_podcasts")
    #recommended_podcast_data = db_cursor.fetchall()

    return render_template(
        'recommendation.html'#,
       # recommended_articles=recommended_articles_data,
       # recommended_videos=recommended_videos_data,
       # recommended_book=recommended_books_data,
       # recommended_podcast=recommended_podcast_data
    )

@app.route('/model.html')
def model():
    return render_template('model.html')

@app.route("/select", methods=["POST"])
def model_select():
    #username = session["username"]
    chat_model = request.form.get("model")
    #date = datetime.now()

    # Store the chat_model in the session
    session["chat_model"] = chat_model
    #print(chat_model)

    return redirect("/chat")


@app.route("/chat")
def chat_ui():
    return render_template("chat.html")

@app.route('/chat_history.html')
def chatHistory():
    return render_template('chat_history.html')

@app.route('/CBT.html')
def cbt():
    return render_template('CBT.html')

@app.route('/questionaire.html')
def stat():
    return render_template('questionaire.html')

@app.route('/activity.html')
def activity():
    return render_template('activity.html')


#Main Execution
if __name__ == "__main__":
    app.run(port=5001)