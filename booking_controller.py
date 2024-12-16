from booking_helper import SentenceParser, DataStore
from similarity import DocumentSimilarity

restaurantFinder = DocumentSimilarity(use_stemming= True)

def find_restaurants(query):
    answers = restaurantFinder.main("Data/restaurants.csv", query)
    ans = []
    for item in answers:
        if 'Answer' in item:  # Ensure the key exists
            ans.append(item['Answer'])
    for x in ans:
        print(f"{x}\n")


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

    find_restaurants(query)

    
    


    