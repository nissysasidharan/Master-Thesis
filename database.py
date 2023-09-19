from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from flask_bcrypt import Bcrypt
from datetime import datetime,date
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Create instances of Flask-SQLAlchemy and Flask-Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

# Define your database models here using SQLAlchemy
class Users(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Chat(db.Model):
    __tablename__ = 'Chat'
    Chat_id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), nullable=False)
    chat_model = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Chat {self.Username} - {self.chat_model}>"

class Messages(db.Model):
    __tablename__ = 'Messages'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer)
    username = db.Column(db.String(255))
    date = db.Column(db.TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=True)
    user_response = db.Column(db.String(255))
    bot_response = db.Column(db.String(255))

    def __repr__(self):
        return f"<Message {self.message_id} - {self.Username}>"
# Define functions to interact with the database
def create_user(username, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = Users(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

def get_latest_chat_id():
    try:
        latest_chat_id = db.session.query(db.func.max(Chat.Chat_id)).scalar()
        return latest_chat_id if latest_chat_id is not None else 0
    except Exception as error:
        print(f"Error fetching latest chat_id: {error}")
        return None

class CBT_Trigger(db.Model):
    __tablename__ = 'CBTTrigger'

    id = db.Column(db.Integer, primary_key=True)
    Tags = db.Column(db.String(255))
    words = db.Column(db.String(255))

class ThoughtDiary(db.Model):
    __tablename__ = 'ThoughtDiary'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    situation = db.Column(db.Text)
    automatic_thoughts = db.Column(db.Text)
    emotions = db.Column(db.Text)
    adaptive_response = db.Column(db.Text)
    outcome = db.Column(db.Text)
    username = db.Column(db.String(255))

    # __repr__ method for ThoughtDiary
    def __repr__(self):
        return f"<ThoughtDiary {self.id} - {self.username}>"


class MoodTracker(db.Model):
    __tablename__ = 'MoodTracker'
    Tracker_Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255))
    tracking_date = db.Column(db.Date)
    sentiment = db.Column(db.String(20))
    chat_id = db.Column(db.Integer)
    Message_id = db.Column(db.Integer)

    # __repr__ method for MoodTracker
    def __repr__(self):
        return f"<MoodTracker {self.Tracker_Id} - {self.Username}>"

class ChatSummary(db.Model):
    __tablename__ = 'ChatSummary'
    history_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    chat_summary = db.Column(db.Text)
    date = db.Column(db.Date)

    # __repr__ method for ChatSummary
    def __repr__(self):
        return f"<ChatSummary {self.history_id} - {self.username}>"

class RecommendedArticle(db.Model):
    __tablename__ = 'recommended_articles'
    ArticleId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    WebLink = db.Column(db.String(255))

class RecommendedVideo(db.Model):
    __tablename__ = 'recommended_videos'
    Id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255))



class RecommendedBook(db.Model):
    __tablename__ = 'recommended_books'
    Id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))

class RecommendedPodcast(db.Model):
    __tablename__ = 'recommended_podcasts'
    Id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255))

class EmotionAnalysis(db.Model):
    __tablename__ = 'EmotionAnalysis'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Responses = db.Column(db.String(255))
    label = db.Column(db.String(255))
    SCORE = db.Column(db.Float)
    Username = db.Column(db.String(255))

# Define the model for Assessment_EmotExperience
class AssessmentEmotExperience(db.Model):
    __tablename__ = 'Assessment_EmotExperience'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    interested = db.Column(db.String(5), nullable=False)
    distressed = db.Column(db.String(5), nullable=False)
    excited = db.Column(db.String(5), nullable=False)
    upset = db.Column(db.String(5), nullable=False)
    strong = db.Column(db.String(5), nullable=False)
    guilty = db.Column(db.String(5), nullable=False)
    scared = db.Column(db.String(5), nullable=False)
    hostile = db.Column(db.String(5), nullable=False)
    enthusiastic = db.Column(db.String(5), nullable=False)
    proud = db.Column(db.String(5), nullable=False)
    irritable = db.Column(db.String(5), nullable=False)
    alert = db.Column(db.String(5), nullable=False)
    ashamed = db.Column(db.String(5), nullable=False)
    inspired = db.Column(db.String(5), nullable=False)
    nervous = db.Column(db.String(5), nullable=False)
    determined = db.Column(db.String(5), nullable=False)
    attentive = db.Column(db.String(5), nullable=False)
    jittery = db.Column(db.String(5), nullable=False)
    active = db.Column(db.String(5), nullable=False)
    afraid = db.Column(db.String(5), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class AssessmentFeedback(db.Model):
    __tablename__ = 'Assessment_Feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    feedback_text = db.Column(db.Text)
    submission_datetime = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class AssessmentUIExperience(db.Model):
    __tablename__ = 'Assessment_UIExperience'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    satisfaction_ui = db.Column(db.Enum('very-dissatisfied', 'dissatisfied', 'neutral', 'satisfied', 'very-satisfied'), nullable=False)
    ease_of_use = db.Column(db.Enum('very-difficult', 'somewhat-difficult', 'neutral', 'somewhat-easy', 'very-easy'), nullable=False)
    welcoming_ui = db.Column(db.Enum('not-welcoming', 'somewhat-welcoming', 'neutral', 'quite-welcoming', 'very-welcoming'), nullable=False)
    scope_purpose_ui = db.Column(db.Enum('not-effective', 'somewhat-effective', 'neutral', 'quite-effective', 'very-effective'), nullable=False)
    impact_ui = db.Column(db.Enum('strongly-negative', 'slightly-negative', 'neutral', 'slightly-positive', 'strongly-positive'), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class AssessmentRecommendation(db.Model):
    __tablename__ = 'Assessment_Recommendation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    tried_recommendations = db.Column(db.Enum('yes', 'no'), nullable=False)
    trust_recommendations = db.Column(db.Enum('completely-trust', 'mostly-trust', 'neutral', 'slightly-distrust', 'strongly-distrust'), nullable=False)
    improvement_suggestions = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class AssessmentDemography(db.Model):
    __tablename__ = 'Assessment_Demography'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    age = db.Column(db.Integer)  # Fixed 'db.column' to 'db.Column'
    gender = db.Column(db.String(255))
    education = db.Column(db.String(255))
    familiarity = db.Column(db.String(255))

class AssessmentModel(db.Model):
    __tablename__ = 'Assessment_ChatbotModel'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    ChatGPT_rating = db.Column(db.Integer)
    BlenderBot_rating = db.Column(db.Integer)
    Dialogpt_rating = db.Column(db.Integer)
    NLPModel_rating = db.Column(db.Integer)
    CounselChatModel_rating = db.Column(db.Integer)
    personality = db.Column(db.Integer)
    responses = db.Column(db.Integer)
    robotic = db.Column(db.Integer)
    concerns = db.Column(db.Integer)
    irrelevant = db.Column(db.Integer)
    handling = db.Column(db.Integer)

class AssessmentInteraction(db.Model):
    __tablename__ = 'Assessment_Interaction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    require_mh_support = db.Column(db.String(255))
    cbt_techniques = db.Column(db.String(10))
    favorite_techniques = db.Column(db.Text)

class AssessmentPrivacy(db.Model):
    __tablename__ = 'Assessment_Privacy'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    personal_info_sharing = db.Column(db.Enum('1', '2', '3', '4', '5'), nullable=False)
    privacy_concerns = db.Column(db.Enum('no-concerns', 'slight-concerns', 'moderate-concerns', 'strong-concerns', 'very-strong-concerns'), nullable=False)
    trust_level = db.Column(db.Enum('completely-trust', 'mostly-trust', 'neutral', 'slightly-distrust', 'strongly-distrust'), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

def get_sentiments(username):
    sentiment_model_name = "finiteautomata/bertweet-base-sentiment-analysis"
    tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
    sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)

    try:


        # Delete existing MoodTracker records for the specified user
        MoodTracker.query.filter_by(Username=username).delete()
        db.session.commit()

        # Retrieve chat messages from the "messages" table
        messages = Messages.query.filter_by(username=username).all()

        sentiments = []

        # Process each chat user response and get its sentiment
        for message in messages:
            user_input = message.user_response
            message_id = message.message_id
            chat_id = message.chat_id
            tracking_date = message.date

            input_ids = tokenizer.encode(user_input, return_tensors="pt")
            logits = sentiment_model(input_ids).logits
            sentiment = logits.argmax().item()
            sentiments.append(sentiment)

            # Insert sentiment, message_id, tracking_date, and username into MoodTracker table
            mood_tracker = MoodTracker(
                tracking_date=tracking_date,
                sentiment=sentiment,
                message_id=message_id,
                username=username,
                chat_id=chat_id
            )
            db.session.add(mood_tracker)

        db.session.commit()
        return sentiments

    except Exception as error:
        print(f"Error processing sentiments: {error}")
        return []

def init_db(app):
    db.init_app(app)
