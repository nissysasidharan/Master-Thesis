import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def train_and_predict_distortions(user_input):
# Load the Excel file into a Pandas DataFrame
    file_path = 'data/cbt_df.csv'  # Replace with the path to your Excel file
    df = pd.read_csv(file_path)

# Define the features (X) and target labels (y)
    X = df['negative_thought']  # Input text (assuming 'negative_thought' contains input text)
    y = df['distortions']  # Target labels (assuming 'distortions' contains distortion labels)

# Create a text classification pipeline
    text_clf = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB()),  # You can choose a different classifier based on your needs
    ])

# Train the model
    text_clf.fit(X, y)



# Use the trained model to predict distortions in the user input
    predicted_distortions = text_clf.predict([user_input])
    return predicted_distortions[0] if predicted_distortions else "No distortions identified in the input."
# Print the identified distortions
#if predicted_distortions:
    #print("Identified Distortions:", predicted_distortions[0])
#else:
    #print("No distortions identified in the input.")
# Get user input
    # user_input = input("Enter your text: ")

# Example usage:
if __name__ == "__main__":
    # file_path = 'data/cbt_df.csv'  # Replace with the path to your Excel file
    user_input = input("Enter your text: ")
    result = train_and_predict_distortions(user_input)
    print("Identified Distortions:", result)
