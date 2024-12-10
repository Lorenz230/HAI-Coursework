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

class TextClassifier:
    def __init__(self, use_stemming=False):
        self.use_stemming = use_stemming
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = None
        self.classifier = None

    def custom_tokenizer(self, text):
        tokens = word_tokenize(text.lower())
        processed_tokens = [
            self.stemmer.stem(word) if self.use_stemming else self.lemmatizer.lemmatize(word)
            for word in tokens if word.isalnum() # and word not in self.stop_words
        ]
        return processed_tokens

    def read_csv_file(self, csv_file):
        df = pd.read_csv(csv_file)
        texts = df['text'].tolist()  # Extract text data
        labels = df['intent'].tolist()  # Extract corresponding labels
        return texts, labels

    def train(self, texts, labels):
        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

        # Fit TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(tokenizer=self.custom_tokenizer, token_pattern=None, ngram_range= (2,2))
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)

        # Train Logistic Regression Model
        self.classifier = LogisticRegression(max_iter=1000, random_state=42)
        self.classifier.fit(X_train_tfidf, y_train)

        # Evaluate on test data
        # y_pred = self.classifier.predict(X_test_tfidf)
        # print("Classification Report:")
        # print(classification_report(y_test, y_pred))
        # print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

    def save_model(self, vectorizer_file, model_file):
        with open(vectorizer_file, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        with open(model_file, 'wb') as f:
            pickle.dump(self.classifier, f)

    def load_model(self, vectorizer_file, model_file):
        with open(vectorizer_file, 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open(model_file, 'rb') as f:
            self.classifier = pickle.load(f)

    def predict(self, query):
        if self.vectorizer is None or self.classifier is None:
            raise ValueError("Model and vectorizer must be loaded or trained before prediction.")
        query_vector = self.vectorizer.transform([query])
        return self.classifier.predict(query_vector)[0]

    def main(self, csv_file, query):
        # Step 1: Read the CSV file
        texts, labels = self.read_csv_file(csv_file)

        # Step 2: Train the classifier
        self.train(texts, labels)

        # Step 3: Save the model and vectorizer
        self.save_model('Data/intentVectorizer.pkl', 'Data/intentModel.pkl')

        # Step 4: Load the model and vectorizer (for testing purposes)
        self.load_model('Data/intentVectorizer.pkl', 'Data/intentModel.pkl')

        # Step 5: Classify a new query
        predicted_label = self.predict(query)
        print(f"Predicted Label for the query '{query}': {predicted_label}")
        return predicted_label
    
# only use when training and evaluating models
# classifier = TextClassifier(use_stemming=False)
# classifier.main("Data/intents_Class.csv", "book table")

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

    def main(self,query):
        # Step 1: Load the model and vectorizer
        self.load_model('Data/identityVectorizer.pkl', 'Data/identityModel.pkl')

        # Step 2: Classify the query
        predicted_label = self.predict(query)
        """
        """
        print(f"Predicted Label for the query '{query}': {predicted_label}")
        return predicted_label

class intentClassifier(TextClassifier):
    def custom_tokenizer(self, text):
        tokens = word_tokenize(text.lower())
        processed_tokens = [
            self.stemmer.stem(word) if self.use_stemming else self.lemmatizer.lemmatize(word)
            for word in tokens if word.isalnum() # and word not in self.stop_words
        ]
        print(processed_tokens)
        return processed_tokens

    def main(self,query):
        # Step 1: Load the model and vectorizer
        self.load_model('Data/intentVectorizer.pkl', 'Data/intentModel.pkl')

        # Step 2: Classify the query
        predicted_label = self.predict(query)
        """
        
        """
        print(f"Predicted Label for the query '{query}': {predicted_label}")
        return predicted_label
