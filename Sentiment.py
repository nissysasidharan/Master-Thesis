from transformers import AutoTokenizer, AutoModelForSequenceClassification
from config import SQLALCHEMY_DATABASE_URI  # Import the SQLAlchemy database URI

from datetime import datetime




def get_sentiments(username):
    sentiment_model_name = "finiteautomata/bertweet-base-sentiment-analysis"
    tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
    sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)

    try:
        # Import MoodTracker model here
        from database import MoodTracker

        # Delete existing MoodTracker records for the specified user
        MoodTracker.query.filter_by(Username=username).delete()
        db.session.commit()

        # Retrieve chat messages from the "messages" table
        from database import Messages  # Import Messages model here
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

if __name__ == "__main__":
    # Initialize the Flask app and SQLAlchemy with your app instance
    from app import app
    db.init_app(app)
    with app.app_context():
        # Replace 'your_username' with the actual username you want to process
        sentiments = get_sentiments('your_username')
        print(sentiments)
