import nltk

nltk.download('punkt')       # For word_tokenize
nltk.download('stopwords')   # For stopwords list
nltk.download('wordnet')     # For WordNet lemmatizer
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

class DocumentSimilarity:

    # Initialises 
    def __init__(self, use_stemming=True):
        self.use_stemming = use_stemming
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = None
        self.tfidf_matrix = None
        self.raw_documents = []
        self.all_files = []
        self.df = None

    # Used to preprocesses text data by tokenizing and normalizing it. 
    # It ensures consistent formatting for the text before analysis
    def custom_tokenizer(self, text):
        # Tokenize the text into individual words (converted to lowercase)
        tokens = word_tokenize(text.lower())
        
        # Process tokens: apply stemming or lemmatization, and filter out stop words
        processed_tokens = []
        for word in tokens:
            if word.isalnum() and word not in self.stop_words:  # Uncomment this if you want to filgter stop words
                if self.use_stemming:
                    processed_tokens.append(self.stemmer.stem(word))  # Apply stemming
                else:
                    processed_tokens.append(self.lemmatizer.lemmatize(word))  # Apply lemmatization
        
        return processed_tokens

        
        
    # This method loads data from a CSV file into the class for processing
    def read_csv_file(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.raw_documents = self.df['Document'].tolist()
        self.all_files = self.df['QuestionID'].tolist()



    # This method converts the documents into TF-IDF vectors. 
    # TF-IDF measures the importance of words in a document relative to a collection (corpus) of documents.
    def fit_tfidf_vectorizer(self):
        self.vectorizer = TfidfVectorizer(
            tokenizer=self.custom_tokenizer,
            token_pattern=None,
            sublinear_tf=True,
            norm='l2',
            use_idf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.raw_documents)
        

    # Calls process_query_and_find_similarities(query) to get a ranked list of (QuestionID, similarity) 
    # pairs using TF-IDF representations.
    # This list contains all documents in descending order of similarity to the query
    def process_query_and_find_similarities(self, query):
        if not self.vectorizer or self.tfidf_matrix.size == 0:
            raise ValueError("Vectoriser not fitted!")

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        return sorted(zip(self.all_files, similarities), key=lambda x: x[1], reverse=True)

    # Calls process_query_and_find_similarities(query) to get a ranked list of (QuestionID, similarity_score) pairs.
    def get_top_results(self, query, similarity_threshold=0.5, top_n=5):
        results = self.process_query_and_find_similarities(query)

        # Filters out results where the similarity score is less than or equal to similarity_threshold.
        filtered_results = [(question_id, similarity) for question_id, similarity in results if similarity > similarity_threshold]

        top_results_array = []
        if filtered_results:
            top_results = sorted(filtered_results, key=lambda x: x[1], reverse=True)[:top_n]

            for question_id, similarity in top_results:
                answer = self.df.loc[self.df['QuestionID'] == question_id, 'Answer'].values[0]
                top_results_array.append({
                    "Question ID": question_id,
                    "Similarity": similarity,
                    "Answer": answer
                })

        else:
            # If filtered_results is empty (i.e., no documents meet the threshold), prints:
            print("I couldnt find what you were looking for, please rephrase:")
        
        return top_results_array

    # Reads csv file, fits the vectoriser and return the results
    def main(self, csv_file, query, similarity_threshold=0.5, top_n=5):
        self.read_csv_file(csv_file)
        self.fit_tfidf_vectorizer()
        results = self.get_top_results(query, similarity_threshold, top_n)
        return results



"""
Subclasses
"""

# subclass that only returns one result rather than multiple
class StopWords(DocumentSimilarity):
    def custom_tokenizer(self, text):
        # Tokenize the text into individual words (converted to lowercase)
        tokens = word_tokenize(text.lower())
        
        # Process tokens: apply stemming or lemmatization, and filter out stop words
        processed_tokens = []
        for word in tokens:
            if word.isalnum(): # and word not in self.stop_words - uncomment this if you want to filgter stop words
                if self.use_stemming:
                    processed_tokens.append(self.stemmer.stem(word))  # Apply stemming
                else:
                    processed_tokens.append(self.lemmatizer.lemmatize(word))  # Apply lemmatization
        
        return processed_tokens

    def get_top_results(self, query, similarity_threshold=0.5, top_n=5):
        results = self.process_query_and_find_similarities(query)

        filtered_results = [(question_id, similarity) for question_id, similarity in results if similarity > similarity_threshold]


        top_results_array = []
        if filtered_results:
            top_results = sorted(filtered_results, key=lambda x: x[1], reverse=True)[:top_n]

            for question_id, similarity in top_results:
                answer = self.df.loc[self.df['QuestionID'] == question_id, 'Answer'].values[0]
                top_results_array.append({
                    "Question ID": question_id,
                    "Similarity": similarity,
                    "Answer": answer
                })
            return top_results_array[0]
                
        else:
            return []


# Subclass that only returns one result
class NoStop(DocumentSimilarity):
    def custom_tokenizer(self, text):
        # Tokenize the text into individual words (converted to lowercase)
        tokens = word_tokenize(text.lower())
        
        # Process tokens: apply stemming or lemmatization, and filter out stop words
        processed_tokens = []
        for word in tokens:
            if word.isalnum() and word not in self.stop_words:  # Uncomment this if you want to filgter stop words
                if self.use_stemming:
                    processed_tokens.append(self.stemmer.stem(word))  # Apply stemming
                else:
                    processed_tokens.append(self.lemmatizer.lemmatize(word))  # Apply lemmatization
        
        return processed_tokens

    def get_top_results(self, query, similarity_threshold=0.8, top_n=5):
        results = self.process_query_and_find_similarities(query)

        filtered_results = [(question_id, similarity) for question_id, similarity in results if similarity > similarity_threshold]


        top_results_array = []
        if filtered_results:
            top_results = sorted(filtered_results, key=lambda x: x[1], reverse=True)[:top_n]

            for question_id, similarity in top_results:
                answer = self.df.loc[self.df['QuestionID'] == question_id, 'Answer'].values[0]
                top_results_array.append({
                    "Question ID": question_id,
                    "Similarity": similarity,
                    "Answer": answer
                })

        
            return top_results_array[0]
        else:
            
            return []

