from booking_helper import SentenceParser, DataStore
from similarity import DocumentSimilarity
import random

restaurantFinder = DocumentSimilarity(use_stemming= True)



def find_restaurants(query):
    while True:
        if query.lower() == "exit":
            print("Exiting the search.")
            return "exit"

        answers = restaurantFinder.main("Data/restaurants.csv", query)

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




def month_selector():
    months = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]

    print("I can show you the available dates for each month. Just pick one:")
    
    # Display numbered options for months
    for i, month in enumerate(months, start=1):
        print(f"{i}: {month}")
    
    while True:  # Loop until a valid input is given
        try:
            choice = int(input("Select the number of the month (1-12): "))
            if 1 <= choice <= 12:
                print(f"You selected: {months[choice - 1]}")
                return months[choice - 1]  # Return the selected month
            else:
                print("Invalid choice. Please select a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a number.")




def day_selector():
    print("Select the day of the month you want to make a reservation for:")

    # Generate up to 15 unique random numbers between 1 and 28
    days = sorted(random.sample(range(1, 29), min(15, 28)))

    # Display the days to the user with keys a, b, c, etc.
    print("Available days:")
    keys = [chr(97 + i) for i in range(len(days))]  # Generate keys 'a', 'b', 'c', ...
    for key, day in zip(keys, days):
        print(f"{key}: Day {day}")

    # Get user input and validate
    while True:
        try:
            user_choice = input("Enter the letter corresponding to your choice: ").strip().lower()

            # Check if the input is a valid key
            if user_choice in keys:
                selected_day = days[keys.index(user_choice)]
                print(f"You have selected Day {selected_day}.")
                return selected_day
                break
            else:
                print(f"Invalid input. Please select a letter between {keys[0]} and {keys[-1]}.")
        except ValueError:
            print("Invalid input. Please enter a valid letter.")
        
def time_selector():
    # Generate six random hours within the range of 10 AM (10) to 12 AM (24)
    hours = random.sample(range(10, 24), 6)

    # Sort the hours to ensure ascending order
    hours.sort()

    # Format the times as strings in HH:00 format
    times = [f"{hour:02d}:00" for hour in hours]

    # Create a lettered list for the user to choose from
    print("Here are the available times:")
    lettered_times = {chr(97 + i): time for i, time in enumerate(times)}  # Create lettered keys 'a', 'b', 'c', ...
    for letter, time in lettered_times.items():
        print(f"{letter}: {time}")

    # Prompt user to select a time frame
    while True:
        selection = input("Select the letter corresponding to your preferred time: ").strip().lower()
        if selection in lettered_times:
            print(f"You selected: {lettered_times[selection]}")
            return lettered_times[selection]
        else:
            print("Invalid selection. Please choose a valid letter from the list.")

def Controller(User_input):

    # When the booking option is chosen this will start processing of the query. 
    parser = SentenceParser()
    parsed_data = parser.main(User_input)
    print(parsed_data)
    data = DataStore()
    data.append_data(location = parsed_data['location'], restaurant_type = parsed_data['restaurant_type'], group_size= parsed_data['group_size'])

    # get location and restaurant type
    data.get_location()
    data.get_restautant_type()
    
    # get location and restaurant type if it is not present.
    booking = data.get_data()
    location = booking['location']
    restaurant_type = booking['restaurant_type']
    query = f"{location}, {restaurant_type}"
    print(f"Searching for {restaurant_type} in {location}")

    # find restaurants after processing query. 
    answer = find_restaurants(query)
    if answer.strip().lower() == "exit":
        return
    
    data.append_data(name = answer, location = location, restaurant_type= restaurant_type)
    
   
    # next step is to find the date for
    print("Almost there, just pick a date and time")
    month = month_selector()
    day = day_selector()
    data.append_data(name = answer, location = location, restaurant_type= restaurant_type, date= f'{day}-{month}')
    print(data.get_data())

    # next pick the time you want to book
    print("You're nearly done, now just pick a time")
    time = time_selector()
    data.append_data(name = answer, location = location, restaurant_type= restaurant_type, date= f'{day}-{month}', time= time)

    
