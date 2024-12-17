import nltk

nltk.download('punkt')       # For word_tokenize
nltk.download('stopwords')   # For stopwords list
nltk.download('wordnet')     # For WordNet lemmatizer



import pandas as pd

class identityManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.load_user_data()

    def load_user_data(self):
        # Loads user data from the specified file.
        try:
            self.df = pd.read_csv(self.file_path, encoding="utf-8", delimiter=",")
        except FileNotFoundError:
            print(f"Error: The file '{self.file_path}' does not exist.")
            self.df = pd.DataFrame(columns=['name'])  # Create a new DataFrame if file is missing

    def check_name(self):
        # Checks if the 'name' column is empty and prompts for input if necessary."""
        if 'name' not in self.df.columns or self.df['name'].dropna().empty:
            print("The 'name' column is empty.")
            name = input("I do not know your name yet, can you tell me? ")
            self.df.at[0, 'name'] = name  # Store the name in the first row of the 'name' column
            self.save_user_data()
            print(f"Hello {name}, How can I help?")
        else:
            name = self.df['name'].iloc[0]
            print(f"Hello {name}, How can I help?")

    def save_user_data(self):
        """Saves the updated user data back to the CSV file."""
        self.df.to_csv(self.file_path, index=False)
    
    def clear_user_data(self):
        """Clears all data in the CSV file."""
        self.df = pd.DataFrame(columns=['name'])  # Reset to an empty DataFrame with the 'name' column
        self.save_user_data()
        # print(f"The file '{self.file_path}' has been cleared.")

# user_data_manager = identityManager("Data/user_data.csv")
# user_data_manager.check_name()