import nltk

nltk.download('punkt')       # For word_tokenize
nltk.download('stopwords')   # For stopwords list
nltk.download('wordnet')     # For WordNet lemmatizer


from classifier import intentClassifier, TextClassifier
from similarity import DocumentSimilarity, StopWords, NoStop
from identity_managment import identityManager
from booking import SentenceParser, DataStore, RestaurantBooking

# make similarity better
classifier = intentClassifier(use_stemming= True)
QAsimilarity = DocumentSimilarity(use_stemming= True)
talkSimilarity = StopWords(use_stemming= True)

dsNoStop = NoStop(use_stemming= True)
dsStop = StopWords(use_stemming= True)

# booking variables
restaurantFinder = DocumentSimilarity(use_stemming=True)
parser = SentenceParser()
data_store = DataStore()
booking_system = RestaurantBooking(restaurantFinder, parser, data_store)


globalIdentityManager = identityManager("Data/user_data.csv")


def handle_talk(user_input):
    answers = talkSimilarity.main("Data/small_talk.csv", user_input)
    # print("DEBUG: Answers returned by talkSimilarity:", answers)  # Debugging line

    if answers:  # Check if there's a valid response
        if isinstance(answers, list):
            top_answer = answers[0]  # Access the first result
            ans = top_answer['Answer']
        elif isinstance(answers, dict):  # Handle a single dictionary response
            ans = answers.get('Answer', "No answer found.")
        else:
            ans = "Invalid format for answers."
        print(ans)
    else:
        print("Sorry, I couldn't find a relevant response.")

def handle_QA(user_input):
    answers = QAsimilarity.main("Data/QA.csv", user_input)
    ans = []
    for item in answers:
        if 'Answer' in item:  # Ensure the key exists
            ans.append(item['Answer'])
    for x in ans:
        print(f"{x}\n")

def handle_identity(user_input):
    user_data_manager = identityManager("Data/user_data.csv")
    user_data_manager.check_name()

def handle_booking(user_input):
    booking_system.controller(user_input)


def handle_mismatch(user_input):
    print("It seems we couldn't determine your intent. Please select from the following options:")
    print("  a) Small Talk")
    print("  b) QA (Question and Answer)")
    print("  c) Identity")
    print("  d) Restaurant Booking")
    
    while True:  # Loop until valid input is received
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

def handle_input(user_input):
    print("Invalid input. Please enter either 'y' for Yes or 'n' for No.")

def chatbot():
    while True:
        user_input = input("Enter something or type 'exit' to end the program: ")
        if user_input.lower() == 'exit':
            globalIdentityManager.clear_user_data()
            print("Goodbye!")
            break
        else:
            answer = dsNoStop.main("Data/intents_noStop.csv", user_input, similarity_threshold= 0.7)
            if answer:
                intent_prediction = answer['Answer'].lower().strip()
                """

                """
                print("prediction",intent_prediction)
                if intent_prediction == "question_answering":
                    handle_QA(user_input)
                elif intent_prediction == "small_talk":
                    handle_talk(user_input)
                elif intent_prediction.strip() == "identity_management":
                    handle_identity(user_input)
                elif intent_prediction == "restaurant_booking":
                    handle_booking(user_input)
                
            else:
                answer = dsStop.main("Data/intents_Stop.csv", user_input, similarity_threshold= 0.65)
                if answer:
                    intent_prediction = answer["Answer"]
                    """
                    
                    """
                    print(f"Stopwords = {intent_prediction}")

                    if intent_prediction == "question_answering":
                        handle_QA(user_input)
                    elif intent_prediction == "small_talk":
                        handle_talk(user_input)
                    elif intent_prediction.strip() == "identity_management":
                        handle_identity(user_input)
                    elif intent_prediction == "restaurant_booking":
                        handle_booking(user_input)
                    

                else:
                    classifier = intentClassifier(use_stemming=False)
                    intent_prediction = classifier.main(csv_file= 'Data/intents_Class.csv', query=user_input)
                    """
                    
                    """
                    print(f"Classifier {intent_prediction}")

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



if __name__ == "__main__":
    chatbot()