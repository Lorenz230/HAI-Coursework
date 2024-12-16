import nltk
from nltk import word_tokenize, pos_tag

# Ensure the necessary data is downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

class SentenceParser:
    def __init__(self):
        self.sentence = None
        self.tokens = []
        self.tags = []

    def set_sentence(self, sentence):
        self.sentence = sentence
        self.tokens = word_tokenize(sentence)
        self.tags = pos_tag(self.tokens)

    def extract_location(self):
        capturing = False
        for word, tag in self.tags:
            if tag == 'IN':
                capturing = True
            elif capturing and tag in {'NNP', 'NNPS'}:
                return word
        return None

    def extract_restaurant_type(self):
        capturing = False
        for word, tag in self.tags:
            if tag in {'DT', 'VB', 'VBP', 'VBZ'}:  # Start capturing after trigger
                capturing = True
            elif capturing:
                if tag in {'JJ', 'NN'}:  # Capture adjective or noun
                    return word
        return None

    def extract_group_size(self):
        group_size = None
        capturing = False
        for word, tag in self.tags:
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

    def parse(self):
        return {
            "location": self.extract_location(),
            "restaurant_type": self.extract_restaurant_type(),
            "group_size": self.extract_group_size()
        }

    def main(self, sentence):
        self.set_sentence(sentence)
        parsed_data = self.parse()
        return parsed_data

class DataStore:
    def __init__(self):
        self.data = []

    def append_data(self, name=None, location=None, restaurant_type=None, group_size=None, date=None, time=None):
        new_entry = {
            "name": name,
            "location": location,
            "restaurant_type": restaurant_type,
            "group_size": group_size,
            "date": date,
            "time": time
        }
        self.data.append(new_entry)

    def get_data(self):
        return self.data
    
    def get_location(self):
        for data in self.data:
            while data['location'] is None:  # Check if the location is None
                location = input("Could you please confirm the location of where you want to book: ")
                data['location'] = location  # Update the location in the entry


