import ast
import sqlite3
import replicate

def get_location_description_query(location):
    return f"""
    Write a 100-word marketing description for visiting {location}.  

    Format it as [<description>]

    Do not add a summary or disclaimer at the beginning or end of your reply. Do not deviate from the format.
    """

def get_location_points_of_interest_query(location):
    return f"""
    Provide 5 points of interest for {location}  

    Format it as <point_of_interest>|<point_of_interest>|<point_of_interest>|<point_of_interest>|<point_of_interest>

    Do not add a summary or disclaimer at the beginning or end of your reply. Do not deviate from the format.
    """

def get_hotel_query_v2(location,country):
    return f"""
    Suggest 20 hotel names for {location} in {country} referencing history and geography where applicable. 
    Avoid cute or tacky references. Avoid references to criminals, natural disasters, or anything in poor taste.
    Don't use names of current popular figures.

    For example, bad hotel names if you're populating Chicago include "The Capone Inn", "The Great Fire Hotel", 
    "Kayne's Kingdom," or "Eddie Vedder's Adventure."  Good names include "The Loop Plaza", "The Chicagoan" 
    or "The Grant Park Hotel".

    Prefer elegance over novelty and avoid alliteration.

    For each hotel provide their star ratings (from 1 to 5, with 5 being the best), addresses, 
    distance in miles from {location} center, and a 50-word description of the hotel.  You must provide an 
    answer even if it's an estimate.

    Format the response as:

    [{{"name":<name>,"address":<address>,"distance":<distance>,"star_rating":star_rating, "description":description}},...]

    Do not add a summary or disclaimer at the beginning or end of your reply. Do not deviate from the format.
    """

def get_room_rate_query_v2(location,country,hotel_name,description):
    return f"""
    For {hotel_name} in {location}, {country} provide 4 different room offers. The hotel is described as {description}.
    Use that description to provide 4 different room offers.
    
    Format it as follows:
    [{{"room_type":<room_type>, "room_description":<room_description>,"amenities":[<list_of_amenities>],"winter_rate":<winter_rate>,"summer_rate":<summer_rate>,"cancellation_policy":cancellation_policy}},...]

    Don't worry if the information isn't up-to-date. Provide a best estimate that matches historical information.  
    For the rates, take into account the seasonality of {location} so higher rates aren't present in the off-season.

    Do not add a summary or disclaimer at the beginning or end of your reply. Do not deviate from the format.
    """

def execute_llm_query(query,max_tokens = 512,model='8'):
    data = replicate.run(
        f"meta/meta-llama-3-{model}b-instruct",
         input={"prompt": query, "max_tokens": max_tokens})

    return "".join(data)

def update_location_description_and_points_of_interest(location,country,model='8'):
        query = get_location_description_query(f"{location},{country}")
        description = execute_llm_query(query,model=model)
        print (description)
        description = description.strip('[').strip(']')
        with sqlite3.connect('travelectable.db') as conn:
            curr = conn.cursor()
            curr.execute("UPDATE destinations SET description = ? WHERE location = ?", (description,location))
            conn.commit()

        query = get_location_points_of_interest_query(f"{location},{country}")
        points_of_interest = execute_llm_query(query,model=model)
        print (points_of_interest)
        points_of_interest = points_of_interest.split('|')
        with sqlite3.connect('travelectable.db') as conn:
            curr = conn.cursor()
            curr.execute("UPDATE destinations SET points_of_interest = ? WHERE location = ?", 
                         (str(points_of_interest),location))
            conn.commit()

def populate_hotels_v2(location_id,location,country,model='8'):
    with sqlite3.connect('travelectable.db') as conn:
        curr = conn.cursor()

        curr.execute("SELECT count(id) FROM hotels WHERE location_id = ?",(location_id,))
        rows = curr.fetchall()
        # We've already populated hotels for this location.
        if rows[0][0] > 0:
            return 

        print(f"Populating hotels for {location} in {country}")

        query = get_hotel_query_v2(location,country)
        hotels = execute_llm_query(query,max_tokens = 1536,model=model)
        hotels = ast.literal_eval(hotels)
        for hotel in hotels:
            new_hotel = (hotel['name'],hotel['address'],hotel['distance'],hotel['star_rating'],
                            hotel['description'],location_id)
            curr.execute("INSERT INTO hotels (name,address,distance,star_rating,description,location_id) "
                                "VALUES (?,?,?,?,?,?)", new_hotel)
            conn.commit()

def populate_room_rates_v2(hotel_id,location,country,hotel_name,description,model='70'):
    with sqlite3.connect('travelectable.db') as conn:
        curr = conn.cursor()

        curr.execute("SELECT count(id) FROM room_rates WHERE hotel_id = ?",(hotel_id,))
        rows = curr.fetchall()
        # We've already populated room rates for this hotel.
        if rows[0][0] > 0:
            return
        
        query = get_room_rate_query_v2(location,country,hotel_name,description)
        room_rates = execute_llm_query(query,max_tokens = 1024,model=model)

        print(f"Populating room rates for {hotel_name} in {location}, {country}")

        room_rates = ast.literal_eval(room_rates)
        with sqlite3.connect('travelectable.db') as conn:
            curr = conn.cursor()
            for room_rate in room_rates:
                new_room_rate = (hotel_id,room_rate['room_type'],room_rate['room_description'],room_rate['winter_rate'],
                                 room_rate['summer_rate'],room_rate['cancellation_policy'],str(room_rate['amenities']))
                curr.execute("INSERT INTO room_rates (hotel_id,room_type,room_description,winter_rate,summer_rate,"
                             "cancellation_policy,amenities) VALUES (?,?,?,?,?,?,?)", new_room_rate)
                conn.commit()
