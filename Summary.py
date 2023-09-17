import mysql.connector
from datetime import datetime
from transformers import pipeline
from config import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE

def summarize_and_insert_summary(username):
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    cursor = db.cursor()

    # Load the summarization pipeline with the CPU version of the model
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", max_length=65)

    # Example usage with SQL query result
    response_query = "SELECT m.user_response, m.bot_response FROM messages m JOIN chat c ON c.chat_id = m.chat_id WHERE c.username = %s;"
    cursor.execute(response_query, (username,))
    result = cursor.fetchall()

    # Combine user and bot responses
    combined_responses = ' '.join([f'{user_response} {bot_response}' for user_response, bot_response in result])

    # Define the sliding window size and step size
    window_size = 512  # Adjust based on your model's maximum sequence length
    step_size = 256  # Adjust based on your preference

    # Initialize summary text
    summary_text = ""

    # Slide the window and summarize each segment
    for i in range(0, len(combined_responses), step_size):
        segment = combined_responses[i:i + window_size]
        summary = summarizer(segment)
        summary_text += summary[0]['summary_text'] + " "

    delete_sql = "DELETE FROM ChatSummary WHERE username = %s"
    cursor.execute(delete_sql, (username,))
    db.commit()
    # Insert the summary into the summary table

    # Insert the summary into the summary table
    current_date = datetime.now()
    insert_query = "INSERT INTO ChatSummary (chat_summary, date, username) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (summary_text, current_date, username))
    db.commit()  # Don't forget to commit the changes

    # Close the database connection
    db.close()


