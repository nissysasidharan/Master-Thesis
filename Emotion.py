import mysql.connector
from transformers import pipeline
from config import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE

def analyze_and_insert_emotions(username):
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = db.cursor()

    # Delete existing records for the username
    #delete_sql = "TRUNCATE TABLE EmotionAnalysis"
    #delete_sql = "DELETE FROM EmotionAnalysis WHERE username = %s"
    #cursor.execute(delete_sql, (username,))
    #cursor.execute(delete_sql)
    #db.commit()
    print(f"Existing records for username '{username}' deleted.")

    # Fetch messages from the database
    select_messages_sql = "SELECT DISTINCT trim(user_response) FROM messages WHERE user_response <> '' and username = %s"
    cursor.execute(select_messages_sql, (username,))
    messages = cursor.fetchall()

    # Create a text classification pipeline for emotion prediction
    pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-emotion-multilabel-latest", top_k=None)

    for message in messages:
        user_response = message[0]
        emotions = pipe(user_response)

        for emotion in emotions[0]:
            label = emotion['label']
            score = emotion['score']
            # Insert emotion data into the table
            insert_emotion_sql = "INSERT INTO EmotionAnalysis (Responses, label, score, username) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_emotion_sql, (user_response, label, score, username))

    # Commit the changes to the database
    db.commit()

    print("Emotion results inserted into the table.")


