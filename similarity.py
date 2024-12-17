import nltk

nltk.download('punkt')       # For word_tokenize
nltk.download('stopwords')   # For stopwords list
nltk.download('wordnet')     # For WordNet lemmatizer



import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

class DocumentSimilarity:
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

    def custom_tokenizer(self, text):
        tokens = word_tokenize(text.lower())
        processed_tokens = [
            self.stemmer.stem(word) if self.use_stemming else self.lemmatizer.lemmatize(word)
            for word in tokens if word.isalnum() and word not in self.stop_words
        ]
        """
        print(f"Processed tokens: {processed_tokens}")
        """
        
        return processed_tokens

    def read_csv_file(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.raw_documents = self.df['Document'].tolist()
        self.all_files = self.df['QuestionID'].tolist()

    def fit_tfidf_vectorizer(self):
        self.vectorizer = TfidfVectorizer(
            tokenizer=self.custom_tokenizer,
            token_pattern=None,
            sublinear_tf=True,
            norm='l2',
            use_idf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.raw_documents)
        """
        print("TF-IDF vectorizer fitted. Shape of TF-IDF matrix:", self.tfidf_matrix.shape)
        """
        
    def process_query_and_find_similarities(self, query):
        if not self.vectorizer or self.tfidf_matrix.size == 0:
            raise ValueError("TF-IDF vectorizer has not been fitted. Call fit_tfidf_vectorizer() first.")

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        """
        print(f"Calculated similarities: {similarities}")
        """
        return sorted(zip(self.all_files, similarities), key=lambda x: x[1], reverse=True)


    def get_top_results(self, query, similarity_threshold=0.5, top_n=5):
        results = self.process_query_and_find_similarities(query)
        """
        print(f"All results: {results}")
        """
        filtered_results = [(question_id, similarity) for question_id, similarity in results if similarity > similarity_threshold]
        """
        print(f"Filtered results (threshold > {similarity_threshold}): {filtered_results}")
        """

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
                """
                print(f"Added to top results: {top_results_array[-1]}")
                """
                
        else:
            print("I couldnt find what you were looking for, please rephrase:")

        
        return top_results_array

    def main(self, csv_file, query, similarity_threshold=0.5, top_n=5):
        self.read_csv_file(csv_file)
        self.fit_tfidf_vectorizer()
        results = self.get_top_results(query, similarity_threshold, top_n)
        return results



"""
Subclasses
"""
# ds = DocumentSimilarity(use_stemming=True)
# ds.main("Data/QA.csv", "stocks and bonds", similarity_threshold=0.45, top_n=5)

class StopWords(DocumentSimilarity):
    def custom_tokenizer(self, text):
        tokens = word_tokenize(text.lower())
        processed_tokens = [
            self.stemmer.stem(word) if self.use_stemming else self.lemmatizer.lemmatize(word)
            for word in tokens if word.isalnum() 
        ]
        """
        print(f"Processed tokens: {processed_tokens}")
        """
        
        return processed_tokens

    def get_top_results(self, query, similarity_threshold=0.5, top_n=5):
        results = self.process_query_and_find_similarities(query)
        """
        print(f"All results: {results}")
        """
        filtered_results = [(question_id, similarity) for question_id, similarity in results if similarity > similarity_threshold]
        """
        print(f"Filtered results (threshold > {similarity_threshold}): {filtered_results}")
        """

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
                """
                print(f"Added to top results: {top_results_array[-1]}")
                """
            return top_results_array[0]
                
        else:
            """
            print("No results above the similarity threshold.")
            """
            
            return []

class NoStop(DocumentSimilarity):
    def custom_tokenizer(self, text):
        tokens = word_tokenize(text.lower())
        processed_tokens = [
            self.stemmer.stem(word) if self.use_stemming else self.lemmatizer.lemmatize(word)
            for word in tokens if word.isalnum() and word not in self.stop_words
        ]
        """
        print(f"Processed tokens: {processed_tokens}")
        """
        
        return processed_tokens

    def get_top_results(self, query, similarity_threshold=0.8, top_n=5):
        results = self.process_query_and_find_similarities(query)
        """
        print(f"All results: {results}")
        """
        filtered_results = [(question_id, similarity) for question_id, similarity in results if similarity > similarity_threshold]
        """
        print(f"Filtered results (threshold > {similarity_threshold}): {filtered_results}")
        """

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
                """
                print(f"Added to top results: {top_results_array[-1]}")
                """
                
            return top_results_array[0]
                
        else:
            """
            print("No results above the similarity threshold.")
            """
            
            return []
        
ds = NoStop(use_stemming=True)
ds.main("Data/QA.csv", "stocks and bonds", similarity_threshold=0.45, top_n=5)