from flask import Flask, render_template, redirect, session, request, flash, jsonify
from database import db, init_db, create_user, Users, Chat, Messages, CBT_Trigger,
import secrets
from config import DATABASE_CONFIG
from datetime import datetime
from chatgpt import start_chatbot
from dialogpt import chat_with_dialogpt
from blenderbot import generate_response



app = Flask(__name__)
# Set the SQLALCHEMY_DATABASE_URI using the configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
)


# Generate a secure secret key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

# Initialize the database with the app
init_db(app)

@app.route('/')
def index():
    return render_template('chat_history.html')



@app.route("/create_user", methods=["GET", "POST"])
def create_user_route():
    if request.method == "POST":
        # Handle the form submission for creating a user
        # Extract the form data and insert it into the database
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Call the function to create the user in the database
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

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the Users table
        user = Users.query.filter_by(username=username).first()

        if user and user.password == password:
            # User exists and password is correct, set the session and redirect to the dashboard
            session['username'] = user.username
            return redirect('/dashboard')
        else:
            # User doesn't exist or password is incorrect, show an error message
            flash('Invalid username or password')

    # If the request method is not POST or login failed, redirect back to the home page
    return redirect('/')

@app.route("/model.html", methods=["GET", "POST"])
def model():
    # Handle the GET request
    return render_template("model.html")

@app.route("/select", methods=["POST"])
def model_select():
    username = session["username"]
    chat_model = request.form.get("model")

    # Store the chat_model in the session
    session["chat_model"] = chat_model

    try:
        # Create a new chat message object and add it to the database session
        chat_message = Chat(username=username, chat_model=chat_model, date=datetime.now())
        db.session.add(chat_message)

        # Commit the changes to the database
        db.session.commit()
    except Exception as error:
        print(f"Error inserting chat data: {error}")

    return redirect("/chat")

@app.route("/chat")
def chat_ui():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    username = request.form.get('username', 'guest')
    user_input = request.form.get("message")
    # chat_model = session.get("chat_model")
    chat_model = "Blenderbot"
    # Fetch only the words from the CBT_Trigger table
    trigger_words = [row.words for row in CBT_Trigger.query.with_entities(CBT_Trigger.words).all()]

    # Check if any trigger words are present in the user's response
    trigger_word_found = any(trigger_word.lower() in user_input.lower() for trigger_word in trigger_words)

    # Determine which chatbot model to use
    if chat_model == "ChatGPT":
        bot_response = start_chatbot(user_input)
    #elif chat_model == 'Dialogpt':
       # bot_response = chat_with_dialogpt(user_input)
    #elif chat_model == 'Blenderbot':
        #bot_response = generate_response(user_input)
    #elif chat_model.lower() == 'nlp chatbot':
       # bot_response = NLP_response(user_input)
    else:
        bot_response = start_chatbot(user_input)

    try:
        # Create a new message and add it to the database session
        new_message = Messages(
            username=username,
            user_response=user_input,
            bot_response=bot_response
        )
        db.session.add(new_message)

        # Commit the changes to the database
        db.session.commit()
    except Exception as error:
        print(f"Error inserting chat data: {error}")

    # Determine whether to show the popup
    #show_popup = trigger_word_found  # Adjust this as needed

    return jsonify({"bot_response": bot_response})

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
