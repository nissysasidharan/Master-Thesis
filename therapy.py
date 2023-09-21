import random
from blenderbot import generate_response
from distortion import train_and_predict_distortions

# Define list of negative thought patterns
negative_thoughts = [
    'All-or-nothing thinking',
    'Overgeneralization',
    'Mental filtering',
    'Discounting the positive',
    'Jumping to conclusions',
    'Magnification and minimization',
    'Emotional reasoning',
    'Should statements',
    'Labeling and mislabeling',
    'Personalization'
]

# Define a list of positive thought patterns
positive_thoughts = [
    'Balanced thinking',
    'Evidence gathering',
    'Identifying exceptions',
    'Thinking in shades of grey',
    'Mindfulness',
    'Gratitude',
    'Self-compassion',
    'Relaxation',
    'Assertiveness',
    'Problem-solving'
]

# Define a function that prompts the user to describe a negative event and uses CBT techniques to help them reframe their thoughts
def cbt_prompt():
    print('Think of a negative event that happened recently. Describe it briefly:')
    event_description = input()
    print('Which of the following negative thought patterns do you think you might be using?')
    for i, thought in enumerate(negative_thoughts):
        print('{}) {}'.format(i + 1, thought))

    thought_index = input('Enter the number of the thought pattern (or type "identify" if you are unsure): ')

    if thought_index.lower() == 'identify':
        user_input = input("Enter your text: ")
        result = train_and_predict_distortions(user_input)
        print("Identified Distortions:", result)  # Trigger the training function
    else:
        try:
            thought_index = int(thought_index) - 1
            if 0 <= thought_index < len(negative_thoughts):
                thought_description = negative_thoughts[thought_index]
                positive_thought_description = positive_thoughts[thought_index]
                print('Okay, it sounds like you might be using {}.'.format(thought_description))
                print('Let\'s try to reframe your thoughts to be more positive.')
                print('What is a more balanced way of thinking about this situation?')
                balanced_thought = input()
                print(
                    'That\'s a great way of thinking about it! Here is a positive thought to replace the negative one:')
                print('{}'.format(positive_thought_description))
                print('{}'.format(balanced_thought))
            else:
                user_input = input("Enter your response: ")  # Prompt user for input
                bot_response = generate_response(user_input)  # Get the response as a string
                print(bot_response)

        except ValueError:
            print('Invalid input. Please enter a valid number.')

# Start the conversation with the user
print('Welcome to the CBTBot. Type something to begin...')

while True:
    try:
        user_input = input()

        # If the user types "help", prompt them to describe a negative event and use CBT techniques to help them reframe their thoughts
        if user_input.lower() == 'help':
            cbt_prompt()

        # If the user's message does not contain the keyword "help", get a response from the bot
        else:
            bot_response = generate_response(user_input)  # Get the response as a string
            print(bot_response)

        if user_input.lower() == 'identify':
            user_input = input("Enter your text: ")
            result = train_and_predict_distortions(user_input)
            print("Identified Distortions:", result)
            break

    except (KeyboardInterrupt, EOFError):
        print('Exiting the CBTBot.')
        break
