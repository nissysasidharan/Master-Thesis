import pandas as pd
from transformers import BartForConditionalGeneration, BartTokenizer

# Read the Excel file
df = pd.read_excel("../data/counsel_chat.xlsx")

# Load the pre-trained BART model and tokenizer
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

# Function to create short answers using text summarization
def create_short_answer(answer):
    inputs = tokenizer.encode("summarize: " + answer, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    short = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return short

# Apply the function to create the 'short_answer' column
df['short_answer'] = df['answerText'].apply(create_short_answer)

# Save the DataFrame to a new Excel file
df.to_excel("../data/shortAnswer.xlsx", index=False)
