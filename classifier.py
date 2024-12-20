import nltk

nltk.download('punkt')       # For word_tokenize
nltk.download('stopwords')   # For stopwords list
nltk.download('wordnet')     # For WordNet lemmatizer
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('universal_tagset')

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.model_selection import train_test_split
import pickle



"""
IMPORTANT: This is the file is used for classifyng texts
"""

# Main TextClassifier class, used for training and testing different classifiers.
class TextClassifier:
    def __init__(self, use_stemming=False):
        self.use_stemming = use_stemming
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = None
        self.classifier = None

     # Tokenises text, lemmatising them and choosing to either remove or keep stop words
    def custom_tokenizer(self, text):
        tokens = word_tokenize(text.lower())
        # Process tokens: apply stemming or lemmatization, and filter out stop words
        processed_tokens = [
            self.stemmer.stem(word) if self.use_stemming else self.lemmatizer.lemmatize(word)
            for word in tokens if word.isalnum() # and word not in self.stop_words
        ]
        return processed_tokens


    # Reads the CSV file for 
    def read_csv_file(self, csv_file):
        df = pd.read_csv(csv_file)
        texts = df['text'].tolist()  # Extract text data
        labels = df['intent'].tolist()  # Extract corresponding labels
        return texts, labels

    def train(self, texts, labels):
        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)


        # Fit TF-IDF Vectorizer
        # Converts text data into numerical feature vectors based on the importance of words in the dataset.
        # The TfidfVectorizer computes the weight of words based on their frequency in the document and their
        #  inverse frequency across all documents.
        self.vectorizer = TfidfVectorizer(tokenizer=self.custom_tokenizer, token_pattern=None, ngram_range= (2,2))
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)


        # Train Logistic Regression Model
        # Uses A classification algorithm that predicts the probability of a class label.
        # It fits a model using the TF-IDF feature matrix (X_train_tfidf) and corresponding labels (y_train).
        self.classifier = LogisticRegression(max_iter=5000, random_state=42)
        self.classifier.fit(X_train_tfidf, y_train)

        """
        Uncomment to run test
        """
        # Evaluate on test data
        # y_pred = self.classifier.predict(X_test_tfidf)
        # print("Classification Report:")
        # print(classification_report(y_test, y_pred))
        # print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")



    # Saves the trained TF-IDF vectoriser and Logistic Regression model to files using pickle
    def save_model(self, vectorizer_file, model_file):
        with open(vectorizer_file, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        with open(model_file, 'wb') as f:
            pickle.dump(self.classifier, f)


    # Loads the saved vectoriser and model from files.
    def load_model(self, vectorizer_file, model_file):
        with open(vectorizer_file, 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open(model_file, 'rb') as f:
            self.classifier = pickle.load(f)


    # Checks if the vectoriser and model are loaded or trained.
    # Transforms the input text (query) into a TF-IDF vector.
    # Uses the Logistic Regression model to predict the class of the query
    def predict(self, query):
        if self.vectorizer is None or self.classifier is None:
            raise ValueError("Model and vectorizer must be loaded or trained before prediction.")
        query_vector = self.vectorizer.transform([query])
        return self.classifier.predict(query_vector)[0]

    # Main fucntion responsible for training, saving and loading vectorizers and models
    def main(self, csv_file, query):
        # Read the CSV file
        texts, labels = self.read_csv_file(csv_file)

        # Train the classifier
        self.train(texts, labels)

        # Save the model and vectorizer
        self.save_model('Data/intentVectorizer.pkl', 'Data/intentModel.pkl')

        # Load the model and vectorizer (for testing purposes)
        self.load_model('Data/intentVectorizer.pkl', 'Data/intentModel.pkl')

        # Step 5: Classify a new query
        predicted_label = self.predict(query)
        
        return predicted_label
    



"""
subclasses - these are ones you will acctually use in code when not training
"""


class identityClassifier(TextClassifier):
    def custom_tokenizer(self, text):
        tokens = word_tokenize(text.lower())
        processed_tokens = [
            self.stemmer.stem(word) if self.use_stemming else self.lemmatizer.lemmatize(word)
            for word in tokens if word.isalnum() and word not in self.stop_words
        ]
        return processed_tokens

    def main(self, csv_file, query):
        # Read the CSV file
        texts, labels = self.read_csv_file(csv_file)

        # Train the classifier
        self.train(texts, labels)

        # Save the model and vectorizer
        self.save_model('Data/identityVectorizer.pkl', 'Data/identityModel.pkl')

        # Load the model and vectorizer (for testing purposes)
        self.load_model('Data/identityVectorizer.pkl', 'Data/identityModel.pkl')

        # Classify a new query
        predicted_label = self.predict(query)
        
        return predicted_label

class intentClassifier(TextClassifier):
    def custom_tokenizer(self, text):
        tokens = word_tokenize(text.lower())
        processed_tokens = [
            self.stemmer.stem(word) if self.use_stemming else self.lemmatizer.lemmatize(word)
            for word in tokens if word.isalnum() # and word not in self.stop_words
        ]
        return processed_tokens
    
    def main(self, csv_file, query):
        # Read the CSV file
        texts, labels = self.read_csv_file(csv_file)

        # Train the classifier
        self.train(texts, labels)

        # Save the model and vectorizer
        self.save_model('Data/intentVectorizer.pkl', 'Data/intentModel.pkl')

        # Load the model and vectorizer (for testing purposes)
        self.load_model('Data/intentVectorizer.pkl', 'Data/intentModel.pkl')

        # Classify a new query
        predicted_label = self.predict(query)
        
        return predicted_label


"""
Run these to ensure ot works on new devices.
"""
classifier = TextClassifier(use_stemming= True)
classifier.main("Data/intents_Class.csv", "book table")

intentsClass = intentClassifier(use_stemming= True)
intentsClass.main("Data/intents_Class.csv", "book table")

identityClass = identityClassifier(use_stemming= True)
predicted_label = identityClass.main("Data/identity.csv", "what is my name?")
