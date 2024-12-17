import nltk

nltk.download('punkt')       # For word_tokenize
nltk.download('stopwords')   # For stopwords list
nltk.download('wordnet')     # For WordNet lemmatizer


from classifier import intentClassifier, TextClassifier
from similarity import DocumentSimilarity, StopWords
from identity_managment import identityManager
from booking import SentenceParser, DataStore, RestaurantBooking

classifier = intentClassifier(use_stemming= True)
QAsimilarity = DocumentSimilarity(use_stemming= True)
talkSimilarity = StopWords(use_stemming= True)


# booking variables
restaurantFinder = DocumentSimilarity(use_stemming=True)
parser = SentenceParser()
data_store = DataStore()
booking_system = RestaurantBooking(restaurantFinder, parser, data_store)


globalIdentityManager = identityManager("Data/user_data.csv")


def handle_talk(user_input):
    answers = talkSimilarity.main("Data/small_talk.csv", user_input)
    ans = answers['Answer']
    print(ans)

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
            intent_prediction = classifier.main(user_input)
            print(intent_prediction)

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