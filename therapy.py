import re

def CBTBot(user_input):
    # Define a dictionary of CBT techniques
    cbt_techniques = {
        'Cognitive restructuring': 'Examining and challenging negative thoughts',
        'Behavioral activation': 'Engaging in activities that give a sense of pleasure or accomplishment',
        'Problem-solving skills training': 'Identifying problems and coming up with practical solutions',
        'Relaxation techniques': 'Engaging in relaxation techniques such as deep breathing, progressive muscle relaxation, or visualization',
        'Exposure therapy': 'Gradually exposing oneself to feared situations or stimuli'
    }

    # Define a list of negative thought patterns
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

    # Define a regular expression pattern for matching messages that contain a CBT technique keyword
    technique_pattern = re.compile(r'(.*)(cognitive restructuring|behavioral activation|problem-solving|relaxation|exposure)(.*)', re.IGNORECASE)

    # Check if the user's message contains a CBT keyword
    match = technique_pattern.search(user_input)
    if match:
        # Identify CBT keyword and describe technique
        technique_keyword = match.group(2).title()
        technique_description = cbt_techniques.get(technique_keyword)
        if technique_description:
            return '{} involves {}'.format(technique_keyword, technique_description)
        else:
            return 'I\'m sorry, I don\'t know much about that technique. Please try another one.'

    # If the user types "help", prompt them to describe a negative event and use CBT techniques to help them reframe their thoughts
    elif user_input.lower() == 'help':
        response = 'Think of a negative event that happened recently. Describe it briefly:\n'
        event_description = input()
        response += 'Which of the following negative thought patterns do you think you might be using?\n'
        for i, thought in enumerate(negative_thoughts):
            response += '{}) {}\n'.format(i + 1, thought)
        thought_index = int(input()) - 1
        thought_description = negative_thoughts[thought_index]
        positive_thought_description = positive_thoughts[thought_index]
        response += 'Okay, it sounds like you might be using {}.\n'.format(thought_description)
        response += 'Let\'s try to reframe your thoughts to be more positive.\n'
        response += 'What is a more balanced way of thinking about this situation?\n'
        balanced_thought = input()
        response += 'That\'s a great way of thinking about it! Here is a positive thought to replace the negative one:\n'
        response += '{}\n'.format(positive_thought_description)
        response += '{}\n'.format(balanced_thought)
        return response

    else:
        return 'I\'m here to help with CBT techniques. You can ask about them or say "help" to get started.'

# Start the conversation with the bot
#print('Welcome to the CBTBot. Type something to begin...')

#while True:
        # try:
        #  user_input = input()
        # bot_response = CBTBot(user_input)
    # print(bot_response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    #except (KeyboardInterrupt, EOFError, SystemExit):
# break
