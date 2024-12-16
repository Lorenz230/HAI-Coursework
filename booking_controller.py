from booking_helper import SentenceParser, DataStore
from similarity import DocumentSimilarity

restaurantFinder = DocumentSimilarity(use_stemming= True)

def find_restaurants(query):
    answers = restaurantFinder.main("Data/restaurants.csv", query)
    numbered_answers = {i + 1: item['Answer'] for i, item in enumerate(answers) if 'Answer' in item}

    print("Here are your top choices:")
    for key, value in numbered_answers.items():
        print(f"{key}: {value}")

    while True:  # Loop until a valid selection is made
        try:
            selection = int(input("Select the number of the option you want: "))
            if selection in numbered_answers:
                print(f"You selected: {numbered_answers[selection]}")
                break  # Exit the loop if valid input is given
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return numbered_answers[selection]

def Controller(User_input):
    # When the booking option is chosen this will start processing of the query. 
    parser = SentenceParser()
    parsed_data = parser.main(User_input)
    print(parsed_data)
    data = DataStore()
    data.append_data(location = parsed_data['location'], restaurant_type = parsed_data['restaurant_type'], group_size= parsed_data['group_size'])

    # get location and restaurant type if it is not present.
    data.get_location()
    data.get_restautant_type()
    
    # get location and restaurant type if it is not present.
    booking = data.get_data()
    location = booking['location']
    restaurant_type = booking['restaurant_type']
    query = f"{location}, {restaurant_type}"
    
    # find restaurants after processing query. 
    answer = find_restaurants(query)
    data.append_data(name = answer, location = location, restaurant_type= restaurant_type)
    print(data.get_data())
    

    


    