from booking_helper import SentenceParser, DataStore
from similarity import DocumentSimilarity

def Controller(User_input):
    # this will run at the start when thre suer asks restaurant booking. 
    parser = SentenceParser()
    parsed_data = parser.main(User_input)
    print(parsed_data)
    data = DataStore()
    data.append_data(location = parsed_data['location'], restaurant_type = parsed_data['restaurant_type'], group_size= parsed_data['group_size'])

    data.get_location()
    
    booking = data.get_data()
    print("booking data:",booking)