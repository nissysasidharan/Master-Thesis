#Imports and Setup

from flask import Flask, render_template, redirect, session, request
import mysql.connector
import secrets
from config import DATABASE_CONFIG
from database import RecommendedArticle, RecommendedVideo, RecommendedBook, RecommendedPodcast

app = Flask(__name__)

# Create a database connection
db_connection = mysql.connector.connect(**DATABASE_CONFIG)
db_cursor = db_connection.cursor()

# Generate a secure secret key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

#Routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    if "username" in session:
        username = session["username"]
        return render_template("dashboard.html", username=username)
    else:
        return redirect("/")

@app.route('/recommendation.html')
def recommended_articles():
    db_cursor.execute("SELECT * FROM recommended_articles")
    recommended_articles_data = db_cursor.fetchall()

    db_cursor.execute("SELECT * FROM recommended_videos")
    recommended_videos_data = db_cursor.fetchall()

    db_cursor.execute("SELECT title,link FROM recommended_books")
    recommended_books_data = db_cursor.fetchall()

    db_cursor.execute("SELECT * FROM recommended_podcasts")
    recommended_podcast_data = db_cursor.fetchall()

    return render_template(
        'recommendation.html',
        recommended_articles=recommended_articles_data,
        recommended_videos=recommended_videos_data,
        recommended_book=recommended_books_data,
        recommended_podcast=recommended_podcast_data
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