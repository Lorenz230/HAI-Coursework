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
            name = input("I do not know your name yet, can you tell me? ")
            self.df.at[0, 'name'] = name  # Store the name in the first row of the 'name' column
            self.save_user_data()
            print(f"Hello {name}")
        else:
            name = self.df['name'].iloc[0]
            print(f"Hello {name}")

        return name


    # Saves the updated user data back to the CSV file 
    def save_user_data(self):
        self.df.to_csv(self.file_path, index=False)
    

    # Clears all data in csv file 
    def clear_user_data(self):
        self.df = pd.DataFrame(columns=['name'])  # Reset to an empty DataFrame with the 'name' column
        self.save_user_data()
        print(f"The file '{self.file_path}' has been cleared.")


    # Returns the name if it is present in the DataFrame.
    def get_name(self):
        
        if 'name' in self.df.columns and not self.df['name'].dropna().empty:
            return self.df['name'].iloc[0]
        return None  # Return None if the name is not present


    # Changes the stored name to a new value
    def change_name(self):
        # Gets input for new name
        new_name = input("What would you like to change your name to? ").strip()
        if new_name: # loops until a name is given
            self.df.at[0, 'name'] = new_name
            self.save_user_data()
            print(f"Your name has been updated to {new_name}.")
        else:
            print("Invalid input. Name was not updated.")


    # view all the bookings the user has made
    def view_bookings(self):
        try:
            # Load the CSV file
            df = pd.read_csv('Data/booking_info.csv')
            
            # Get the name to filter bookings
            name = self.get_name()
            
            # Filter the DataFrame for rows where the 'booker' matches the name
            filtered_df = df[df['booker'] == name]
            
            # Check if any bookings match the name
            if not filtered_df.empty:  # Corrected: no parentheses here
                print("Bookings Data for:", name)
                print(filtered_df)
            else:
                print(f"No bookings found for booker: {name}")
            
            # Return the filtered DataFrame for further use if needed
            return filtered_df
        except FileNotFoundError:
            print(f"Error: File not found.")


    # Responsible for predicting user intent when identity managment is chosen
    def main(self, predicted_label):

        # formats the predicted label properly
        predicted_label = predicted_label.strip().lower()

        # Handles if user wnts to know their name
        if predicted_label == 'identify':
            name = self.get_name()
            if name == None:
                self.check_name()
            else:
                print("your name is ", name)
        
        # Handles if user wnats to change thier name
        elif predicted_label == 'identity_change':
            self.change_name()

        # Handles if user wants to view bookings
        elif predicted_label == 'view_bookings':
            self.view_bookings()