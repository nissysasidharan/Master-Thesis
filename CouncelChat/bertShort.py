import pandas as pd
from summarizer import Summarizer

# Read the Excel file
df = pd.read_excel("../data/counsel_chat.xlsx")

# Load the BERT extractive summarizer
model = Summarizer()

# Function to create short answers using BERT extractive summarization
def create_short_answer(answer):
    short = model(answer, ratio=0.3)  # Adjust ratio as needed
    return short

# Apply the function to create the 'short_answer' column
df['short_answer'] = df['answerText'].apply(create_short_answer)
print(df)
# Save the DataFrame to a new Excel file
df.to_excel("../data/shortAnswer.xlsx", index=False)
