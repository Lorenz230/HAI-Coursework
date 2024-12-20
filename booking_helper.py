import nltk

nltk.download('punkt')       # For word_tokenize
nltk.download('stopwords')   # For stopwords list
nltk.download('wordnet')     # For WordNet lemmatizer
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('universal_tagset')

import nltk
from nltk import word_tokenize, pos_tag
from similarity import DocumentSimilarity, StopWords

# Ensure the necessary data is downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


"""

IMPORTANT: This is the booking helper file, repsonsible for parsing user inputs and managing booking data

"""


# Parses user query when finding restaurants to identify location and restaurany type
class SentenceParser:
    def __init__(self):
        self.sentence = None
        self.tokens = []
        self.tags = []


    # Tokenizes and applies POS tagging to sentance or user input
    def set_sentence(self, sentence):
        self.sentence = sentence
        self.tokens = word_tokenize(sentence)
        self.tags = pos_tag(self.tokens)


    # Extracts the location in the sentance
    def extract_location(self):
        capturing = False
        for word, tag in self.tags:
            if tag == 'IN':
                capturing = True
            elif capturing and tag in {'NNP', 'NNPS'}:
                return word
        return None
    

    # Extracts the type of Restaurant
    def extract_restaurant_type(self):
        capturing = False
        for word, tag in self.tags:
            if tag in {'DT', 'VB', 'VBP', 'VBZ'}:  # Start capturing after trigger
                capturing = True
            elif capturing:
                if tag in {'JJ', 'NN'}:  # Capture adjective or noun
                    return word
        return None


    # Parses the data, extracing location and restaurant type
    def parse(self):
        return {
            "location": self.extract_location(),
            "restaurant_type": self.extract_restaurant_type(),
        }

    # Runs the code to parse the sentance and get info
    def main(self, sentence):
        self.set_sentence(sentence)
        parsed_data = self.parse()
        return parsed_data

# Class used for storing data about booking information
class DataStore:
    def __init__(self):
        self.data = None
        self.similarity = DocumentSimilarity()  # Create an instance of DocumentSimilarity

    # Appends data, default being None.
    def append_data(self, name=None, location=None, restaurant_type=None, group_size=None, date=None, time=None, booker = None):
        
        # Appends data
        self.data = {
            "name": name,
            "location": location,
            "restaurant_type": restaurant_type,
            "group_size": group_size,
            "date": date,
            "time": time,
            "booker": booker
        }

    # Returns booking data
    def get_data(self):
        return self.data
    

    # Returns location
    def get_location(self):
        # Ensures that location is not None, loops until it isn't. 
        if self.data and self.data['location'] is None:
            while self.data['location'] is None:  # Check if the location is None
                location = input("Could you please confirm the location of where you want to book: ")
                self.data['location'] = location  # Update the location in the entry


    # Returns the restaurant type
    def get_restautant_type(self):
        # Ensures that location is not None, loops until it isn't. 
        if self.data and self.data['restaurant_type'] is None:
            while self.data['restaurant_type'] is None:  # Check if the restaurant type is None
                location = input("Could you please confirm what type of food you would like to eat: ")
                self.data['restaurant_type'] = location  # Update the restaurant in the entry


    # Changes location of booking
    def change_location(self):
        location = input("Could you please confirm the location of where you want to boo -  ")
        self.data['location'] = location  # Update the location in the entry
        

    # Changes restaurant type
    def change_restaurant_type(self):
        location = input("Could you please confirm what type of food you would like to eat -  ")
        self.data['restaurant_type'] = location  # Update the restaurant in the entry