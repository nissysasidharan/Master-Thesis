import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

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

# Get user input
user_input = input("Enter your text: ")

# Use the trained model to predict distortions in the user input
predicted_distortions = text_clf.predict([user_input])

# Print the identified distortions
if predicted_distortions:
    print("Identified Distortions:", predicted_distortions[0])
else:
    print("No distortions identified in the input.")
