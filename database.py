from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
def init_db(app):
    db.init_app(app)


class EmotionAnalysis(db.Model):
    __tablename__ = 'emotionanalysis'
    id = db.Column(db.Integer, primary_key=True)
    Responses = db.Column(db.Text)
    label = db.Column(db.String(255))
    SCORE = db.Column(db.Float)
    Username = db.Column(db.String(255))

    def __repr__(self):
        return f"<EmotionAnalysis {self.id} - {self.Username}>"

class Users(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Chat(db.Model):
    __tablename__ = 'Chat'
    Chat_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    chat_model = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Chat {self.username} - {self.chat_model}>"


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

class CBT_Trigger(db.Model):
    __tablename__ = 'CBT_Trigger'

    id = db.Column(db.Integer, primary_key=True)
    Tags = db.Column(db.String(255))
    words = db.Column(db.String(255))

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
