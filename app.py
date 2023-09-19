from flask import Flask, render_template, redirect, session, request, flash, jsonify, url_for
from database import db, init_db, create_user, Users, Chat, Messages, CBT_Trigger, EmotionAnalysis, ThoughtDiary, \
    MoodTracker, get_sentiments, AssessmentDemography, AssessmentModel, AssessmentInteraction, AssessmentPrivacy, \
    AssessmentRecommendation, AssessmentFeedback, AssessmentEmotExperience, AssessmentUIExperience, \
    RecommendedVideo, RecommendedArticle, RecommendedBook, RecommendedPodcast
import secrets
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import distinct, text
from datetime import datetime, date
from chatgpt import start_chatbot
#from dialogpt import chat_with_dialogpt
#from blenderbot import generate_response

app = Flask(__name__)
# Set the SQLALCHEMY_DATABASE_URI using the configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = (
# f"mysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
# )
# Use this SQLAlchemy database URI in your Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Generate a secure secret key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

# Initialize the database with the app
init_db(app)
messages = []

@app.route('/')
def index():
    return render_template('chat.html', messages=messages)

def create_user(Username, email, password):
    try:
        new_user = Users(Username=Username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return True  # User created successfully
    except Exception as error:
        print(f"Error creating user: {error}")
        return False  # Error creating user

# Function to check if a user exists and validate the password
def check_user(Username, password):
    try:
        user = Users.query.filter_by(Username=Username).first()

        if user is None:
            return False  # User does not exist

        # Validate the password using bcrypt or another secure method
        # For example, using bcrypt:
        # if bcrypt.check_password_hash(user.password, password):
        if user.password == password:
            return True  # Login successful
        else:
            return False  # Incorrect password

    except Exception as error:
        print(f"Error checking user: {error}")
        return False  # Error checking user


@app.route("/create_user", methods=["GET", "POST"])
def create_user_route():
    if request.method == "POST":
        # Handle the form submission for creating a user
        # Extract the form data and insert it into the database
        Username = request.form["Username"]
        email = request.form["email"]
        password = request.form["password"]

        # Call the function to create the user in the database (using database.py)
        if create_user(Username, email, password):
            # If user creation is successful, redirect to the dashboard
            session['username'] = Username
            return redirect('/dashboard')
        else:
            # If user creation fails, show an error message
            flash("Error creating user.", "error")

    return render_template("home.html")


@app.route("/consent", methods=["GET", "POST"])
def consent():
    if request.method == "POST":
        # Handle the form submission for creating a user
        # Extract the form data and insert it into the database
        Username = request.form["Username"]
        email = request.form["email"]
        password = request.form["password"]

        # Call the function to create the user in the database (using database.py)
        if create_user(Username, email, password):
            # If user creation is successful, redirect to the dashboard
            session['Username'] = Username
            return redirect('/home')
        else:
            # If user creation fails, show an error message
            flash("Error creating user.", "error")

    return render_template("home.html")


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        Username = request.form['Username']
        password = request.form['password']

        # Check if the user exists in the database and validate the password
        if check_user(Username, password):
            # User is authenticated, store their username in the session
            session['Username'] = Username
            return redirect('/dashboard')
        else:
            # Invalid credentials, show an error message
            flash('Invalid username or password', 'error')
            return redirect('/')

    return redirect('/')


@app.route("/dashboard")
def dashboard():
    if "Username" in session:
        Username = session["Username"]
        return render_template("dashboard.html", Username=Username)
    else:
        return redirect("/")

@app.route('/recommendation.html')
def recommended_articles():
    recommended_articles_data = db.session.execute(text("SELECT * FROM recommended_articles")).fetchall()
    recommended_videos_data = db.session.execute(text("SELECT * FROM recommended_videos")).fetchall()
    recommended_books_data = db.session.execute(text("SELECT * FROM recommended_books")).fetchall()
    recommended_podcast_data = db.session.execute(text("SELECT * FROM recommended_podcasts")).fetchall()

    return render_template(
        'recommendation.html',
        recommended_articles=recommended_articles_data,
        recommended_videos=recommended_videos_data,
        recommended_books=recommended_books_data,
        recommended_podcast=recommended_podcast_data
    )


@app.route("/model.html", methods=["GET", "POST"])
def model():
    username = 'SRH'
    # Handle the GET request
    return render_template("model.html")


@app.route("/select", methods=["POST"])
def model_select():
    username = 'SRH'
    chat_model = request.form.get("model")
    date = datetime.now()

    # Store the chat_model in the session
    session["chat_model"] = chat_model
    print(chat_model)

    # Insert the chat data into the database
    try:
        new_message = Chat(Username=username, chat_model=chat_model, date=date)
        db.session.add(new_message)
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
    #trigger_words = [row.words for row in CBT_Trigger.query.with_entities(CBT_Trigger.words).all()]

    # Check if any trigger words are present in the user's response
    #trigger_word_found = any(trigger_word.lower() in user_input.lower() for trigger_word in trigger_words)

    # print(trigger_words)
    #print(trigger_word_found)

    bot_response = start_chatbot(user_input)
    print(bot_response)

    messages.append({'user': user_input, 'bot': bot_response})

    return {'bot_response': bot_response}

    #new_message = Messages(username=username, user_response=user_input, bot_response=bot_response)
    #db.session.add(new_message)
    #db.session.commit()

    # Determine whether to show the popup
    #show_popup = trigger_word_found  # Adjust this as needed

    # Pass the bot_response and other data to the chat.html template
    #return render_template("chat.html", bot_response=bot_response, user_input=user_input#, show_popup=show_popup
                          # )



@app.route("/handle_popup_response", methods=["GET", "POST"])
def handle_popup_response():
    if request.method == "POST":
        # Process the popup response
        popup_response = request.form.get("popup_response")

        if popup_response == "yes":
            return redirect("/thought_diary")
        elif popup_response == "no":
            return redirect("/chat")
        else:
            return redirect("/chat")
    else:
        # Handle the case when the route is accessed with a different method (e.g., GET)
        print("Invalid Method:", request.method)
        return redirect("/chat")  # Or return an error response


@app.route("/thought_diary", methods=["GET", "POST"])
def thought_diary_post():
    if request.method == "POST":
        username = session["username"]
        current_date = date.today().strftime("%Y-%m-%d")
        situation = request.form["situation"]
        automatic_thoughts = request.form["automatic_thoughts"]
        emotions = request.form["emotions"]
        adaptive_response = request.form["adaptive_response"]
        outcome = request.form["outcome"]

        # Insert the thought entry into the database
        thoughts = ThoughtDiary.query.filter_by(username=username).all()
        db.session.add(thoughts)
        db.session.commit()

        # Redirect to the chat page after handling the form submission
        return redirect("/chat")

    # Handle GET requests separately if needed
    # ...

    # Return the Thought Diary page template
    return render_template("thought_diary.html")



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


@app.route('/chat_history')
def thought_entries_and_mood_tracker():
    username = 'SRH'

    # Query Thought Diary entries and Mood Tracker data
    entries = ThoughtDiary.query.with_entities(
        ThoughtDiary.date,
        ThoughtDiary.situation,
        ThoughtDiary.automatic_thoughts,
        ThoughtDiary.emotions,
        ThoughtDiary.adaptive_response,
        ThoughtDiary.outcome
    ).filter_by(username=username).all()

    distinct_dates = db.session.query(distinct(Chat.date)). \
        join(MoodTracker, Chat.Chat_id == MoodTracker.chat_id). \
        filter(Chat.Username == username).all()

    print(distinct_dates)

    # Assuming distinct_dates is a list of date objects
    formatted_dates = [date[0].strftime('%d-%m-%Y') for date in distinct_dates]

    # Print the formatted dates
    print(formatted_dates)

    distinct_responses = db.session.query(distinct(EmotionAnalysis.Responses)).filter_by(Username=username).all()

    # Extract the response values from the query result
    distinct_response_values = [response[0] for response in distinct_responses]

    return render_template('chat_history.html', thought_entries=entries,
                           mood_tracker_data=formatted_dates,
                           emotion_data=distinct_response_values)


@app.route('/aemotional', methods=['POST'])
def emot_experience():
    if request.method == 'POST':
        username = 'SRH'
        interested = request.form.get('Interested')
        distressed = request.form.get('Distressed')
        excited = request.form.get('Excited')
        upset = request.form.get('Upset')
        strong = request.form.get('Strong')
        guilty = request.form.get('Guilty')
        scared = request.form.get('Scared')
        hostile = request.form.get('Hostile')
        enthusiastic = request.form.get('Enthusiastic')
        proud = request.form.get('Proud')
        irritable = request.form.get('Irritable')
        alert = request.form.get('Alert')
        ashamed = request.form.get('Ashamed')
        inspired = request.form.get('Inspired')
        nervous = request.form.get('Nervous')
        determined = request.form.get('Determined')
        attentive = request.form.get('Attentive')
        jittery = request.form.get('Jittery')
        active = request.form.get('Active')
        afraid = request.form.get('Afraid')

        # Create an instance of AssessmentEmotExperience
        emot_experience_entry = AssessmentEmotExperience(
            username=username,
            interested=interested,
            distressed=distressed,
            excited=excited,
            upset=upset,
            strong=strong,
            guilty=guilty,
            scared=scared,
            hostile=hostile,
            enthusiastic=enthusiastic,
            proud=proud,
            irritable=irritable,
            alert=alert,
            ashamed=ashamed,
            inspired=inspired,
            nervous=nervous,
            determined=determined,
            attentive=attentive,
            jittery=jittery,
            active=active,
            afraid=afraid
        )

        # Add and commit the emot experience entry to the database
        db.session.add(emot_experience_entry)
        db.session.commit()

    return render_template('questionaire.html')
@app.route('/afeedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        username = 'SRH'
        feedback_text = request.form.get('feedback-text')

        # Create an instance of AssessmentFeedback
        feedback_entry = AssessmentFeedback(
            username=username,
            feedback_text=feedback_text
        )

        # Add and commit the feedback entry to the database
        db.session.add(feedback_entry)
        db.session.commit()

    return render_template('questionaire.html')

@app.route('/auiexperience', methods=['POST'])
def ui_experience():
    if request.method == 'POST':
        username = 'SRH'
        satisfaction_ui = request.form.get('satisfaction-ui')
        ease_of_use = request.form.get('ease-of-use')
        welcoming_ui = request.form.get('welcoming-ui')
        scope_purpose_ui = request.form.get('scope-purpose-ui')
        impact_ui = request.form.get('impact-ui')

        # Create an instance of AssessmentUIExperience
        assessment = AssessmentUIExperience(
            username=username,
            satisfaction_ui=satisfaction_ui,
            ease_of_use=ease_of_use,
            welcoming_ui=welcoming_ui,
            scope_purpose_ui=scope_purpose_ui,
            impact_ui=impact_ui
        )

        # Add and commit the assessment to the database
        db.session.add(assessment)
        db.session.commit()

    return render_template('questionaire.html')  # Redirect to a success page after submission

@app.route('/arecommendation', methods=['POST'])
def assessment_recommendation():
    if request.method == 'POST':
        username = 'SRH'
        tried_recommendations = request.form.get('tried-recommendations')
        print(tried_recommendations)
        trust_recommendations = request.form.get('trust-recommendations')
        print(trust_recommendations)
        improvement_suggestions = request.form.get('improvement-suggestions')
        print(improvement_suggestions)

        # Create an instance of AssessmentRecommendation
        assessment = AssessmentRecommendation(
            username=username,
            tried_recommendations=tried_recommendations,
            trust_recommendations=trust_recommendations,
            improvement_suggestions=improvement_suggestions
        )

        # Add and commit the assessment to the database
        db.session.add(assessment)
        db.session.commit()

    return render_template('questionaire.html')
@app.route('/aprivacy', methods=['POST'])
def assessment_privacy():
    if request.method == 'POST':
        username = 'SRH'
        personal_info_sharing = request.form.get('personal-info-sharing')
        privacy_concerns = request.form.get('privacy-concerns')
        trust_level = request.form.get('trust-level')

        # Create an instance of AssessmentPrivacy
        privacy_assessment = AssessmentPrivacy(
            username=username,
            personal_info_sharing=personal_info_sharing,
            privacy_concerns=privacy_concerns,
            trust_level=trust_level
        )

        # Add and commit the assessment to the database
        db.session.add(privacy_assessment)
        db.session.commit()

    return render_template('questionaire.html')

@app.route('/ainteraction', methods=['POST'])
def assessment_interaction():
    if request.method == 'POST':
        username = 'SRH'
        require_mh_support = request.form.get('require_mh_support')
        cbt_techniques = request.form.get('cbt-techniques')
        favorite_techniques = request.form.get('favorite-techniques')

        # Create an instance of AssessmentInteraction
        assessment = AssessmentInteraction(
            username=username,
            require_mh_support=require_mh_support,
            cbt_techniques=cbt_techniques,
            favorite_techniques=favorite_techniques
        )

        # Add and commit the assessment to the database
        db.session.add(assessment)
        db.session.commit()

    return render_template('questionaire.html')

@app.route('/achatbotmodel', methods=['POST'])
def chatbot_model_assessment():
    if request.method == 'POST':
        # Get data from the form
        username = 'SRH'
        ChatGPT_rating = request.form['ChatGPT_rating']
        BlenderBot_rating = request.form['BlenderBot_rating']
        Dialogpt_rating = request.form['Dialogpt_rating']
        NLPModel_rating = request.form['NLPModel_rating']
        CounselChatModel_rating = request.form['CounselChatModel_rating']
        personality_engaging = request.form['personality']  # Corrected key
        responses_clear = request.form['responses']  # Corrected key
        responses_robotic = request.form['robotic']  # Corrected key
        understood_inputs = request.form['concerns']  # Corrected key
        irrelevant_responses = request.form['irrelevant']  # Corrected key
        error_handling = request.form['handling']  # Corrected key

        # Create an instance of AssessmentChatbotModel
        assessment = AssessmentModel(
            username=username,
            ChatGPT_rating=ChatGPT_rating,
            BlenderBot_rating=BlenderBot_rating,
            Dialogpt_rating=Dialogpt_rating,
            NLPModel_rating=NLPModel_rating,
            CounselChatModel_rating=CounselChatModel_rating,
            personality=personality_engaging,
            responses=responses_clear,
            robotic=responses_robotic,
            concerns=understood_inputs,
            irrelevant=irrelevant_responses,
            handling=error_handling
        )

        # Add and commit the assessment to the database
        db.session.add(assessment)
        db.session.commit()


    return render_template('questionaire.html')
@app.route('/ademographic', methods=['POST'])
def assessment():
    if request.method == 'POST':
        username = 'SRH'
        # Get data from the form

        age = request.form['age']
        gender = request.form['gender']
        education = request.form['education']
        familiarity = request.form['familiarity']



        # Create an instance of AssessmentDemography
        demography = AssessmentDemography(username=username, age=age, gender=gender, education=education, familiarity=familiarity)


        # Insert data into the Assessment_Demography table
        db.session.add(demography)
        db.session.commit()

    return render_template('questionaire.html')

if __name__ == "__main__":
    app.run(debug=True)
