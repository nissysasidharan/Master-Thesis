import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-400M-distill")

# Define a function to generate a response
def generate_response(user_input, chat_history=None, max_response_length=1024):
    # Ensure that user_input is of type str
    user_input = str(user_input)

    # Tokenize user input
    input_ids = tokenizer.encode(user_input, return_tensors="pt", max_length=max_response_length, truncation=True)

    # Explicitly convert input_ids to LongTensor
    input_ids = input_ids.to(torch.long)

    if chat_history is not None:
        # Append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history, input_ids], dim=-1)
    else:
        bot_input_ids = input_ids

    # Generate a response from the model
    bot_input_ids = bot_input_ids.to(model.device)  # Ensure bot_input_ids is on the same device as the model
    response_ids = model.generate(bot_input_ids, max_length=max_response_length, num_return_sequences=1)

    # Decode the response and remove special tokens
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response, bot_input_ids  # Return bot_input_ids to update chat_history

# Main loop for interacting with the chatbot
chat_history = None  # Initialize chat history as None
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response, bot_input_ids = generate_response(user_input, chat_history)
    print("Bot:", response)

    # Update chat history
    chat_history = bot_input_ids
