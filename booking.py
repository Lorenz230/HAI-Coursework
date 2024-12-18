import nltk

nltk.download('punkt')       # For word_tokenize
nltk.download('stopwords')   # For stopwords list
nltk.download('wordnet')     # For WordNet lemmatizer


from booking_helper import SentenceParser, DataStore
from similarity import DocumentSimilarity
import random
from identity_managment import identityManager






class RestaurantBooking:
    def __init__(self, restaurant_finder, parser, data_store, IdentityManager):
        self.restaurant_finder = restaurant_finder
        self.parser = parser
        self.data_store = data_store
        self.IdentityManager = IdentityManager

    def find_restaurants(self, query):
        while True:
            if query.lower() == "exit":
                print("Exiting the search.")
                return "exit"

            answers = self.restaurant_finder.main("Data/restaurants.csv", query)

            if answers:  # If answers are found, proceed
                numbered_answers = {i + 1: item['Answer'] for i, item in enumerate(answers) if 'Answer' in item}

                print("Here are your top choices:")
                for key, value in numbered_answers.items():
                    print(f"{key}: {value}")

                while True:  # Loop until a valid selection is made
                    try:
                        selection = int(input("Select the number of the option you want: "))
                        if selection in numbered_answers:
                            print(f"You selected: {numbered_answers[selection]}")
                            return numbered_answers[selection]  # Return the selected answer
                        else:
                            print("Invalid choice. Please select a number from the list.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:  # If no answers are found, prompt the user for a new query
                print("No restaurants found. Please refine your search or type 'exit' to quit.")
                query = input("Enter a new search query: ")


    def refine_query(self, user_input):
        parsed_data = self.parser.main(user_input)
        self.data_store.append_data(
            location=parsed_data['location'], 
            restaurant_type=parsed_data['restaurant_type'], 
        )

        while True:  # Loop until user confirms the query
            booking_data = self.data_store.get_data()
            location = booking_data.get('location')
            restaurant_type = booking_data.get('restaurant_type')

            print(f"Searching for {restaurant_type} in {location}")

            # Ask user for confirmation
            confirmation = input(f"Confirm search query? Location: '{location}', Restaurant type: '{restaurant_type}' (yes/no): ").strip().lower()

            if confirmation in ['yes', 'y']:
                query = f"{location},{restaurant_type}"
                print(f"Finalized Query: Searching for {restaurant_type} in {location}")
                return query  # Return the finalized query

            elif confirmation in ['no', 'n']:
                # Allow user to modify location and restaurant type
                change_location = input("Do you want to change the location? (yes/no): ").strip().lower()
                if change_location in ['yes', 'y']:
                    self.data_store.change_location()

                change_restaurant = input("Do you want to change the restaurant type? (yes/no): ").strip().lower()
                if change_restaurant in ['yes', 'y']:
                    self.data_store.change_restaurant_type()

            else:
                print("Invalid input. Please type 'yes' to confirm or 'no' to make changes.")

    def month_selector(self):
        months = [
            "January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"
        ]

        print("I can show you the available dates for each month. Just pick one:")
        
        for i, month in enumerate(months, start=1):
            print(f"{i}: {month}")
        
        while True:
            try:
                choice = int(input("Select the number of the month (1-12): "))
                if 1 <= choice <= 12:
                    print(f"You selected: {months[choice - 1]}")
                    return months[choice - 1]
                else:
                    print("Invalid choice. Please select a number between 1 and 12.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def day_selector(self):
        print("Select the day of the month you want to make a reservation for:")
        days = sorted(random.sample(range(1, 29), min(15, 28)))
        print("Available days:")

        keys = [chr(97 + i) for i in range(len(days))]
        for key, day in zip(keys, days):
            print(f"{key}: Day {day}")

        while True:
            user_choice = input("Enter the letter corresponding to your choice: ").strip().lower()
            if user_choice in keys:
                selected_day = days[keys.index(user_choice)]
                print(f"You have selected Day {selected_day}.")
                return selected_day
            else:
                print(f"Invalid input. Please select a letter between {keys[0]} and {keys[-1]}.")

    def pick_date_and_time(self, answer):
        print("Almost there, just pick a date and time")
        month = self.month_selector()
        day = self.day_selector()
        booking_data = self.data_store.get_data()
        location = booking_data.get('location')  # Set location to current stored value
        restaurant_type = booking_data.get('restaurant_type')

        self.data_store.append_data(
            name=answer, 
            location=location,  # Use current location
            restaurant_type=restaurant_type, 
            date=f'{day}-{month}'
        )
        return day, month  # Return day and month

    def time_selector(self):
        hours = random.sample(range(10, 24), 6)
        hours.sort()
        times = [f"{hour:02d}:00" for hour in hours]

        print("Here are the available times:")
        lettered_times = {chr(97 + i): time for i, time in enumerate(times)}
        for letter, time in lettered_times.items():
            print(f"{letter}: {time}")

        while True:
            selection = input("Select the letter corresponding to your preferred time: ").strip().lower()
            if selection in lettered_times:
                print(f"You selected: {lettered_times[selection]}")
                return lettered_times[selection]
            else:
                print("Invalid selection. Please choose a valid letter from the list.")

    def pick_time(self):
        print("You're nearly done, now just pick a time")
        time = self.time_selector()
        booking_data = self.data_store.get_data()
        location = booking_data.get('location')  # Set location to current stored value
        restaurant_type = booking_data.get('restaurant_type')
        date = booking_data.get('date')
        answer = booking_data.get('name')

        self.data_store.append_data(
            name=answer, 
            location=location,  # Use current location
            restaurant_type=restaurant_type, 
            date=date,
            time=time
        )

    def get_group_size(self):
        while True:
            try:
                group_size = int(input("How many people is the table for? "))
                if group_size > 0:
                    print(f"Booking for {group_size} people confirmed.")
                    return group_size
                else:
                    print("Please enter a valid number greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    def confirm_size(self):
        print("So close...")
        size = self.get_group_size()
        booking_data = self.data_store.get_data()
        location = booking_data.get('location')  # Set location to current stored value
        restaurant_type = booking_data.get('restaurant_type')
        date = booking_data.get('date')
        answer = booking_data.get('name')
        time = booking_data.get('time')

        self.data_store.append_data(
            name=answer, 
            location=location,  # Use current location
            restaurant_type=restaurant_type, 
            date=date,
            time=time,
            group_size = size
        )



    def confirm_booker(self):
        print("Last step...")
        booker = self.IdentityManager.get_name()
        if booker is not None:
            while True:
                choice = input(f"Do you want me to use '{booker}' or a different name? \n"
                            "Choice: a) use my name, b) pick a different one\n"
                            "Type choice: ").strip().lower()
                if choice == 'a':
                    # Use the current name
                    print(f"Using the name: {booker}")
                    break
                elif choice == 'b':
                    # Allow the user to change the name
                    self.IdentityManager.change_name()
                    booker = self.IdentityManager.get_name()
                    break
                else:
                    # Handle invalid input
                    print("Invalid choice. Please type 'a' to use the current name or 'b' to change it.")
        else:
            # Handle case where no name is found after all checks
            print("No valid name was provided. Please set a name.")
            booker = self.IdentityManager.change_name()
            print(f"Name set to: {booker}")

        # Retrieve the current stored booking data
        booking_data = self.data_store.get_data()
        location = booking_data.get('location')  # Set location to current stored value
        restaurant_name = booking_data.get('name')  # Name of the restaurant
        restaurant_type = booking_data.get('restaurant_type')
        date = booking_data.get('date')
        time = booking_data.get('time')
        size = booking_data.get('group_size')

        # Append data with the correct names
        self.data_store.append_data(
            name=restaurant_name,  # Restaurant name
            location=location,     # Use current location
            restaurant_type=restaurant_type,
            date=date,
            time=time,
            group_size=size,
            booker=booker  # Ensure the updated 'booker' is passed here
        )

        

    def confirm_booking(self):
        print("\nPlease review your booking details:")
        booking_data = self.data_store.get_data()

        # Function to display booking summary
        def display_booking_summary():
            print("\n--- Booking Summary ---")
            print(f"Name: {booking_data.get('booker', 'N/A')}")
            print(f"Restaurant: {booking_data.get('name', 'N/A')}")
            print(f"Location: {booking_data.get('location', 'N/A')}")
            print(f"Restaurant Type: {booking_data.get('restaurant_type', 'N/A')}")
            print(f"Date: {booking_data.get('date', 'N/A')}")
            print(f"Time: {booking_data.get('time', 'N/A')}")
            print(f"Group Size: {booking_data.get('group_size', 'N/A')} people")
            print("-------------------------\n")

        # Display initial booking summary
        display_booking_summary()

        # Ask for confirmation
        while True:
            choice = input("Do you want to confirm this booking? (yes/no): ").strip().lower()
            if choice in ['yes', 'y']:
                print("Booking confirmed! Thank you for choosing our service.")
                return True  # Booking is confirmed
            elif choice in ['no', 'n']:
                print("Booking cancelled. Would you like to modify any of the details?")
                print("Options:")
                print("a) Date")
                print("b) Time")
                print("c) Group Size")
                print("d) Booking Name")
                print("e) Cancel Booking")
                
                while True:
                    change_choice = input("Select an option to modify (a-f): ").strip().lower()
                    if change_choice == 'a':
                        print("Let's change the date.")
                        day, month = self.pick_date_and_time(booking_data['name'])
                        booking_data['date'] = f"{day}-{month}"

                        print("sinece we changed the date, you must pick the time again")
                        new_time = self.time_selector()
                        booking_data['time'] = new_time

                    elif change_choice == 'b':
                        print("Let's change the time.")
                        new_time = self.time_selector()
                        booking_data['time'] = new_time
                    elif change_choice == 'c':
                        print("Let's change the group size.")
                        new_size = self.get_group_size()
                        booking_data['group_size'] = new_size
                    elif change_choice == 'd':
                        print("Let's change the booking name.")
                        self.IdentityManager.change_name()
                        new_name = self.IdentityManager.get_name()
                        print("New name == ", new_name)
                        booking_data['booker'] = new_name
                    elif change_choice == 'e':
                        print("Booking cancelled. Let us know if you need help again!")
                        return False  # Booking is cancelled
                    else:
                        print("Invalid option. Please select a valid option (a-f).")
                        continue

                    print("Details updated. Here's the updated booking summary:")
                    display_booking_summary()  # Show updated booking details
                    break  # Exit modification loop and show updated summary
            else:
                print("Invalid input. Please type 'yes' to confirm or 'no' to modify/cancel.")




    def controller(self, user_input):

        
    
        # refine the query the user has given.
        query = self.refine_query(user_input)
        
        # find restaurants based on query
        answer = self.find_restaurants(query)
        if answer.strip().lower() == "exit":
            return
        
        # select date and time
        self.pick_date_and_time(answer)
        

        # select time
        self.pick_time()
        

        # confirm group size
        self.confirm_size()
        

        # select name for booking
        self.confirm_booker()

        print("Data ====== ", self.data_store.get_data())
        
        
        # confirm the booking
        self.confirm_booking()
    



# restaurantFinder = DocumentSimilarity(use_stemming=True)
# parser = SentenceParser()
# data_store = DataStore()
# booking_system = RestaurantBooking(restaurantFinder, parser, data_store)
# booking_system.controller("to eat indian food in Nottingham")

