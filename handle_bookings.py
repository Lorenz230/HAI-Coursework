import nltk
from nltk import word_tokenize, pos_tag

# Ensure the necessary data is downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define the sentence
sentence = "show me Italian restaurants around Nottingham with 4 adults"
# Tokenize and tag the sentence
tokens = word_tokenize(sentence)
tags = pos_tag(tokens)
# Extract the primary location (proper noun)
def extract_location(tags):
    word = None
    capturing = False
    for word, tag in tags:
        if tag == 'IN':
            capturing = True
        elif capturing and tag in {'NNP', 'NNPS'}:
            return word
    return None

# Extract the restaurant type
def extract_restaurant_type(tags):
    word = None
    capturing = False
    for word, tag in tags:
        if tag in {'DT', 'VB', 'VBP', 'VBZ'}:  # Start capturing after trigger
            capturing = True
        elif capturing:
            if tag in {'JJ', 'NN'}:  # Capture adjective or noun
                return word
    return None

def extract_group_size(tags):
    group_size = None  # Initialize group_size to None
    capturing = False
    for word, tag in tags:
        if tag == 'IN':  # Trigger capturing after "for"
            capturing = True
        elif capturing:
            if tag == 'CD':  # Capture the number (e.g., "4", "2")
                group_size = word
            elif tag in {'NN', 'NNS'}:  # Ensure it refers to group descriptor
                if word.lower() not in {'pm', 'am', 'oclock', "o'clock", 'Oclock', "O'clock"}:
                    return group_size  # Return the number if descriptor matches
                else:
                    capturing = False  # Stop capturing if unrelated descriptor
            else:  # Stop if unrelated tags appear
                capturing = False
    return None





# Extract and print the location and restaurant type
location = extract_location(tags)
restaurant_type = extract_restaurant_type(tags)
group_size = extract_group_size(tags)

print("Tags:", tags)
print("Location:", location)
print("Restaurant Type:", restaurant_type)
print("group size:", group_size)