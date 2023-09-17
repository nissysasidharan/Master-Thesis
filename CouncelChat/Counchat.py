import pandas as pd
import numpy as np
import os
import json
import pickle
import pandas as pd
import scipy
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('bert-base-nli-mean-tokens')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn import svm
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
from nltk.corpus import stopwords
import nltk
nltk.download('averaged_perceptron_tagger')
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import string
import re
import pickle

lemmatizer = WordNetLemmatizer()

import warnings
from sklearn.exceptions import DataConversionWarning

warnings.filterwarnings("ignore", category=DataConversionWarning)

# Define the directory path
data_directory = "../data/"

# Load the pickle files from the specified directory
count_vect_path = os.path.join(data_directory, "count_vect_svm.pkl")
transformer_path = os.path.join(data_directory, "transformer_svm.pkl")
svm_model_path = os.path.join(data_directory, "model_svm.pkl")

Count_Vect = pickle.load(open(count_vect_path, "rb"))
Transf_Vect = pickle.load(open(transformer_path, "rb"))
SVM_tf = pickle.load(open(svm_model_path, "rb"))

# Define the directory path
data_directory = "../data/"
data_path = os.path.join(data_directory, "updatedCC.csv")

cls = ['Anger Management', 'Behavioral Change', 'Counseling Fundamentals',
       'Depression', 'Family Conflict', 'Intimacy', 'LGBTQ',
       'Marriage', 'Parenting', 'Relationship Dissolution', 'Relationships',
       'Self-esteem', 'Sleep Improvement', 'Social Relationships', 'Stress/Anxiety',
       'Substance Abuse/Addiction', 'Trauma/Grief/Loss', 'Workplace issues']


def load_excel_data(data_path):
    df = pd.read_csv(data_path)
    return df


def sentiment_analyzer(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # oject gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] > 0.2:
        return ("Positive")

    else:
        return ("Negative")


def Classify_problem(msg):
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    text = msg.replace('\d+', '')
    text = text.replace('[^\w\s]', '')
    text = text.lower()

    text = [lemmatizer.lemmatize(item, tag_dict.get(pos_tag([item])[0][1][0].upper(), wordnet.NOUN)) for item in
            word_tokenize(text)]
    text = ' '.join(text)

    #   Predict Probabilities With tfidf-SVM,RF
    counts = Count_Vect.transform([text])
    counts = Transf_Vect.transform(counts)
    tfidf_svm = SVM_tf.predict_proba(counts)

    maxpos = tfidf_svm.argmax()
    label = cls[maxpos]
    return label

def get_category_responses(category, user_input):
    df = load_excel_data(data_path)
    category = category.lower()
    filtered_df = df[df['topic'] == category]
    queries = filtered_df['questionTitle'].tolist()
    return df, queries

def similarity_test(query, user_input_embedding):
    query_embeddings = model.encode([query])  # Encode the query
    user_input_embedding_2d = user_input_embedding.reshape(1, -1)  # Reshape user_input_embedding to 2D
    scores = []

    for query_embedding in query_embeddings:
        distances = scipy.spatial.distance.cdist([query_embedding], user_input_embedding_2d, "cosine")[0]
        score = 1 - distances
        scores.extend(score)

    return scores

# Define a dictionary of common general questions and answers
common_questions_and_answers = {
    "Hi": "I am a Nex chatbot.",
    "Hello": "I am a Nex chatbot.",
    "How are you?": "I am doing good. How about you?",
    "What is your name?": "I am a Nex chatbot.",
    "How are you doing?": "I'm just a computer program, so I don't have feelings, but I'm here to help you!",
    "Tell me a joke.": "Sure, here's one: Why don't scientists trust atoms? Because they make up everything!",
    "See you later.": "Sure",
    "Goodbye!": "Goodbye"
}

# ... (previous code)

if __name__ == "__main__":
    print("Chatbot: Hi! How can I assist you today?")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "bye":
            print("Chatbot: Goodbye! If you have more questions in the future, feel free to ask.")
            break

        # Check if the user's input matches any of the common general questions
        if user_input in common_questions_and_answers:
            answer = common_questions_and_answers[user_input]
            print("Chatbot:", answer)
        else:
            sentiment_result = sentiment_analyzer(user_input)
            Classify_problem = Classify_problem(user_input.lower())
            user_input_embedding = model.encode(user_input)  # Embed the user input

            df, get_category_responses_list = get_category_responses(Classify_problem, user_input)

            similarity_scores = []
            for query in get_category_responses_list:
                score = similarity_test(query, user_input_embedding)
                similarity_scores.append(score)

            max_score_idx = np.argmax(similarity_scores)
            best_matching_question = get_category_responses_list[max_score_idx]

            answer_text = df[df['questionTitle'] == best_matching_question]['answerText'].iloc[0]

            print("Sentiment:", sentiment_result)
            print("Classify_problem:", Classify_problem)
            print("get_category_responses:", get_category_responses_list)
            print("Best matching question:", best_matching_question)
            print("Answer Text:", answer_text)
            print("Similarity score:", similarity_scores[max_score_idx])

            # Wait for the chatbot to respond
            print("Chatbot: Is there anything else you would like to ask?")

