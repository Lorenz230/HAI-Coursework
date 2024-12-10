from classifier import intentClassifier, TextClassifier

classifier = intentClassifier(use_stemming= True)

def handle_talk(user_input):
    print("small_talk")

def handle_QA(user_input):
    print("QA")

def handle_identity(user_input):
    print("ID")

def handle_booking(user_input):
    print("booking")

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
                        handle_talk(user_input)
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
                        handle_talk(user_input)
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
                        handle_talk(user_input)
                        break  # Exit the loop for confirmation input
                    elif intent_confirm in ["n", "no"]:
                        handle_mismatch(user_input)
                        break  # Exit the loop for confirmation input
                    else:
                        handle_input(user_input)  # Inform user and retry
                

if __name__ == "__main__":
    chatbot()