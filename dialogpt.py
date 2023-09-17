import warnings
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Suppress the warning
warnings.filterwarnings("ignore", message="A decoder-only architecture is being used, but right-padding was detected!")

# Initialize the tokenizer with padding_side='left'
tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-large', padding_side="left")

# Initialize the model
model = AutoModelForCausalLM.from_pretrained('microsoft/DialoGPT-large', config={'pad_token_id': tokenizer.eos_token_id})

# Initialize chat history as None
chat_history = None

# Define a function to generate a response
def chat_with_dialogpt(user_input, chat_history):
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Append the new user input tokens to the chat history
    if chat_history is not None:
        bot_input_ids = torch.cat([chat_history, new_user_input_ids], dim=-1)
    else:
        bot_input_ids = new_user_input_ids

    # Generate a response from the chatbot
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=100,
        top_p=0.7,
        temperature=0.8
    )

    # Decode and return the chatbot's response
    chat_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return chat_response, bot_input_ids

# Main loop for interacting with the chatbot
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break  # Exit the chatbot if the user types 'exit'

    chat_response, chat_history = chat_with_dialogpt(user_input, chat_history)
    print(f"Chatbot: {chat_response}")
