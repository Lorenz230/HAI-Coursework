import nltk

nltk.download('punkt')       # For word_tokenize
nltk.download('stopwords')   # For stopwords list
nltk.download('wordnet')     # For WordNet lemmatizer
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')

from classifier import intentClassifier, TextClassifier, identityClassifier
from similarity import DocumentSimilarity, StopWords, NoStop
from identity_managment import identityManager
from booking import SentenceParser, DataStore, RestaurantBooking

"""

IMPORTANT: This is the main file responsible for STARTING THE PROGRAM
"""

# Classifier used for predicitng intent
classifier = intentClassifier(use_stemming= True)

# Classifier for preciting identity intent
userClassifier = identityClassifier(use_stemming=False)

# Cosine similarity for question answering
QAsimilarity = DocumentSimilarity(use_stemming= True)

# Cosine similarity for small talk
talkSimilarity = StopWords(use_stemming= True)

# Cosine similarity subclasss that removes stop words
dsNoStop = NoStop(use_stemming= True)

# Cosine similarity subclasss that doesnt remove words
dsStop = StopWords(use_stemming= True)

#Identity manager for managing information
globalIdentityManager = identityManager("Data/user_data.csv")

# Cosine similarity fpr finding the relevant restaurants
restaurantFinder = DocumentSimilarity(use_stemming=True)

# POS tagger to identify key words 
parser = SentenceParser()

# Stores all necessray booking info
data_store = DataStore()

# Instance of restaurant booking class
booking_system = RestaurantBooking(restaurantFinder, parser, data_store,globalIdentityManager)


# Handles small talk intent
def handle_talk(user_input):

    # Finds cosine similarity between user input and data in small_talk.csv
    answers = talkSimilarity.main("Data/small_talk.csv", user_input)
    
    # gets user name
    name = globalIdentityManager.get_name()

    if answers:  # Check if there's a valid response over the threshold
        if isinstance(answers, list):
            top_answer = answers[0]  # Access the first result
            ans = top_answer['Answer']
        elif isinstance(answers, dict):  # Handle a single dictionary response
            ans = answers.get('Answer', "No answer found.")
        else:
            ans = "Invalid format for answers."

        # Modify the answer if conditions are met
        if name is not None:
            greetings = ["hello", "hi", "hey"]
            for greeting in greetings:
                if greeting in ans.lower():
                    ans = ans.lower().replace(greeting, f"{greeting} {name}").capitalize()
                    break

            # Check for '?' and add name before it
            if '?' in ans:
                ans = ans.replace('?', f' {name}?')

        print(ans)
    else:
        print("Sorry, I couldn't find a relevant response.")


# Handles question and Answering intent
def handle_QA(user_input):
    # Gets answers from cosinne similarity
    answers = QAsimilarity.main("Data/QA.csv", user_input)
    ans = []
    
    # Prints out all of the answers above the threshold
    for item in answers:
        if 'Answer' in item:  # Ensure the key exists
            ans.append(item['Answer'])
    for x in ans:
        print(f"{x}\n")


# Handles handle identoty intent
def handle_identity(user_input):
    
    identity_prediction = userClassifier.main(csv_file= 'Data/identity.csv', query=user_input)   
    globalIdentityManager.main(predicted_label= identity_prediction)
    

# Handles booking intent
def handle_booking(user_input):
    booking_system.controller(user_input)


# Handles incorrect predicitons and asks the user for confirmation
def handle_mismatch(user_input):

    # Displays options
    print("It seems we couldn't determine your intent. Please select from the following options:")
    print("  a) Small Talk")
    print("  b) QA (Question and Answer)")
    print("  c) Identity")
    print("  d) Restaurant Booking")
    
    # Loop until a valid intent is picked
    while True:
        user_choice = input("Your choice (a, b, c, d): ").strip().lower()
        
        if user_choice == 'a':
            handle_talk(user_input)
            break
        elif user_choice == 'b':
            handle_QA(user_input)
            break
        elif user_choice == 'c':
            handle_identity(user_input)
            break
        elif user_choice == 'd':
            handle_booking(user_input)
            break
        else:
            print("Invalid choice. Please enter 'a', 'b', 'c', or 'd'.")


# Handles inputs when Classifier gets intent wrong.
def handle_input(user_input):
    print("Invalid input. Please enter either 'y' for Yes or 'n' for No.")


# Handles the main flow ofthe ChatBot
def chatbot():
    while True:
        user_input = input("Enter something or type 'exit' to end the program: ")

        # Clears user name when exiting program
        if user_input.lower() == 'exit':
            globalIdentityManager.clear_user_data()
            print("Goodbye!")
            break
        else:
            # Uses cosine similarioty to predict intent, removing stop words in the process
            answer = dsNoStop.main("Data/intents_noStop.csv", user_input, similarity_threshold= 0.7)
            if answer:
                # Ensures that intent is in the correct format.
                intent_prediction = answer['Answer'].lower().strip()
                # print("prediction",intent_prediction)
                
                if intent_prediction == "question_answering":
                    handle_QA(user_input)

                elif intent_prediction == "small_talk":
                    handle_talk(user_input)

                elif intent_prediction.strip() == "identity_management":
                    handle_identity(user_input)

                elif intent_prediction == "restaurant_booking":

                    while True:  # Loop until valid input is received
                        intent_confirm = input(
                            "Did you want to make a restaurant reservation?\n"
                            "  y) Yes\n"
                            "  n) No\n"
                            "Your choice: "
                        ).strip().lower()

                        if intent_confirm in ["y", "yes"]:
                            handle_booking(user_input)
                            break  # Exit the loop for confirmation input
                        elif intent_confirm in ["n", "no"]:
                            handle_mismatch(user_input)
                            break  # Exit the loop for confirmation input
                        else:
                            handle_input(user_input)  # Inform user and retry
                    
                    
            # Same process as the one above, keeping the stop signs this time
            else:
                answer = dsStop.main("Data/intents_Stop.csv", user_input, similarity_threshold= 0.65)
                if answer:
                    intent_prediction = answer["Answer"]
                    #print(f"Stopwords = {intent_prediction}")

                    if intent_prediction == "question_answering":
                        handle_QA(user_input)

                    elif intent_prediction == "small_talk":
                        handle_talk(user_input)

                    elif intent_prediction.strip() == "identity_management":
                        handle_identity(user_input)

                    elif intent_prediction == "restaurant_booking":
                        while True:  # Loop until valid input is received
                            intent_confirm = input(
                                "Did you want to make a restaurant reservation?\n"
                                "  y) Yes\n"
                                "  n) No\n"
                                "Your choice: "
                            ).strip().lower()

                            if intent_confirm in ["y", "yes"]:
                                handle_booking(user_input)
                                break  # Exit the loop for confirmation input
                            elif intent_confirm in ["n", "no"]:
                                handle_mismatch(user_input)
                                break  # Exit the loop for confirmation input
                            else:
                                handle_input(user_input)  # Inform user and retry
                        
                    
                # Same process as the other two, this time using classifier and asking user for confirmation on all intents
                else:
                    classifier = intentClassifier(use_stemming=False)
                    intent_prediction = classifier.main(csv_file= 'Data/intents_Class.csv', query=user_input)

                    # Small-talk loop
                    if intent_prediction.strip().lower() == "small_talk":
                        while True:  # Loop until valid input is received
                            intent_confirm = input(
                                "Did you want to make small talk?\n"
                                "  y) Yes\n"
                                "  n) No\n"
                                "Your choice: "
                            ).strip().lower()

                            if intent_confirm in ["y", "yes"]:
                                handle_talk(user_input)
                                break  # Exit the loop for confirmation input
                            elif intent_confirm in ["n", "no"]:
                                handle_mismatch(user_input)
                                break  # Exit the loop for confirmation input
                            else:
                                handle_input(user_input)  # Inform user and retry

                    # Question answering loop
                    if intent_prediction.strip().lower() == "question_answering":
                        while True:  # Loop until valid input is received
                            intent_confirm = input(
                                "Did you want me to answer some general QA questions?\n"
                                "  y) Yes\n"
                                "  n) No\n"
                                "Your choice: "
                            ).strip().lower()

                            if intent_confirm in ["y", "yes"]:
                                handle_QA(user_input)
                                break  # Exit the loop for confirmation input
                            elif intent_confirm in ["n", "no"]:
                                handle_mismatch(user_input)
                                break  # Exit the loop for confirmation input
                            else:
                                handle_input(user_input)  # Inform user and retry

                    # Booking loop
                    if intent_prediction.strip().lower() == "restaurant_booking":
                        while True:  # Loop until valid input is received
                            intent_confirm = input(
                                "Did you want to make a restaurant reservation?\n"
                                "  y) Yes\n"
                                "  n) No\n"
                                "Your choice: "
                            ).strip().lower()

                            if intent_confirm in ["y", "yes"]:
                                handle_booking(user_input)
                                break  # Exit the loop for confirmation input
                            elif intent_confirm in ["n", "no"]:
                                handle_mismatch(user_input)
                                break  # Exit the loop for confirmation input
                            else:
                                handle_input(user_input)  # Inform user and retry

                    # Identity management loop
                    if intent_prediction.strip().lower() == "identity_management":
                        while True:  # Loop until valid input is received
                            intent_confirm = input(
                                "Did you want some user data?\n"
                                "  y) Yes\n"
                                "  n) No\n"
                                "Your choice: "
                            ).strip().lower()

                            if intent_confirm in ["y", "yes"]:
                                handle_identity(user_input)
                                break  # Exit the loop for confirmation input
                            elif intent_confirm in ["n", "no"]:
                                handle_mismatch(user_input)
                                break  # Exit the loop for confirmation input
                            else:
                                handle_input(user_input)  # Inform user and retry


# Runs program
if __name__ == "__main__":
    chatbot()