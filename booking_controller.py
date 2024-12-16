from booking_helper import SentenceParser, DataStore
from similarity import DocumentSimilarity

restaurantFinder = DocumentSimilarity(use_stemming= True)

def find_restaurants(query):
    answers = restaurantFinder.main("Data/restaurants.csv", query)
    numbered_answers = {i + 1: item['Answer'] for i, item in enumerate(answers) if 'Answer' in item}

    print(f"Here are your top Choices:")
    for key, value in numbered_answers.items():
        print(f"{key}: {value}")

    print("select the number of the option you want")

def Controller(User_input):
    # this will run at the start when thre suer asks restaurant booking. 
    parser = SentenceParser()
    parsed_data = parser.main(User_input)
    print(parsed_data)
    data = DataStore()
    data.append_data(location = parsed_data['location'], restaurant_type = parsed_data['restaurant_type'], group_size= parsed_data['group_size'])

    data.get_location()
    
    booking = data.get_data()
    location = booking['location']
    restaurant_type = booking['restaurant_type']
    query = f"{location}, {restaurant_type}"
    
    #find restaurants after processing query. 
    find_restaurants(query)

    
    


    