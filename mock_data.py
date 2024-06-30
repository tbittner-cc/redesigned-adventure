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

def get_hotel_query(radius,location,lat,long):
    return f"""
    List 10 hotels within {radius} miles of {location[1]} at lat/long ({lat},{long}).

    Provide their star ratings, addresses, distance in miles from lat/long ({lat},{long}), 
    and a 50-word description of the hotel.  You must provide an answer even if it's an estimate.

    Format the response as:

    [{{"name":<name>,"address":<address>,"distance":<distance>,"star_rating":star_rating, "description":description}},...]

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

def get_room_rate_query(location,hotel_name,address):
    return f"""
    For {hotel_name} at {address} in {location[1]}, provide 4 different room offers. Format it as follows:
    [{{"room_type":<room_type>, "room_description":<room_description>,"amenities":[<list_of_amenities>],"winter_rate":<winter_rate>,"summer_rate":<summer_rate>,"cancellation_policy":cancellation_policy}},...]

    Don't worry if the information isn't up-to-date. Provide a best estimate that matches historical information.  
    For the rates, take into account the seasonality of {location[1]} so higher rates aren't present in the off-season.

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

def populate_location_description_and_points_of_interest(location):
    with sqlite3.connect('travel_data.db') as conn:
        curr = conn.cursor()
        curr.execute("SELECT id,description,points_of_interest FROM destinations WHERE id = ?", (location[0],))
        rows = curr.fetchall()
        data = rows[0]

    if data[1] == '' or data[1] is None:
        query = get_location_description_query(location[1])
        description = execute_llm_query(query)
        description = description.strip('[').strip(']')
        with sqlite3.connect('travel_data.db') as conn:
            curr = conn.cursor()
            curr.execute("UPDATE destinations SET description = ? WHERE id = ?", (description,location[0]))
            conn.commit()

    if data[2] == '' or data[2] is None:
        query = get_location_points_of_interest_query(location[1])
        points_of_interest = execute_llm_query(query)
        points_of_interest = points_of_interest.split('|')
        with sqlite3.connect('travel_data.db') as conn:
            curr = conn.cursor()
            curr.execute("UPDATE destinations SET points_of_interest = ? WHERE id = ?", 
                         (str(points_of_interest),location[0]))
            conn.commit()

def populate_hotels(location):
    with sqlite3.connect('travel_data.db') as conn:
        curr = conn.cursor()
        curr.execute("SELECT id,name,address FROM hotels WHERE location_id = ?", (location[0],))
        rows = curr.fetchall()
        # We're gating the number of hotels for each location to 25
        if len(rows) >= 25:
            return

        print(f"Populating hotels for {location[1]}")
        print(f"Number of hotels: {len(rows)}")

        hotel_names = [row[1] for row in rows]
        hotel_addresses = [row[2] for row in rows]

        curr.execute("SELECT latitude,longitude,distance_tried FROM destinations WHERE id = ?", 
                     (location[0],))
        data = curr.fetchall()
        (lat,long,radius) = data[0]

        # We've reached a large enough radius for this.  We'll go with what we have.
        if radius >= 25:
            return

        new_hotels_found = False

        query = get_hotel_query(radius,location,lat,long)
        hotels = execute_llm_query(query,max_tokens = 1024)
        # The 8b context LLM seems to struggle with closing the list.
        if hotels[-1] != ']':
            hotels += ']'
        # And adding the appropriate quotes
        hotels = hotels.replace('"address": ', '"address": "').replace('""','"')
        try:
            hotels = ast.literal_eval(hotels)
        except Exception as e:
            print(e)
            print(hotels)
        for hotel in hotels:
            # There's no guarantee that everything will be formatted properly, but
            # we can limit the number of duplicates by checking the name and address.
            if hotel['name'] in hotel_names or hotel['address'] in hotel_addresses:
                continue
            else:
                new_hotels_found = True
                new_hotel = (hotel['name'],hotel['address'],hotel['distance'],hotel['star_rating'],
                                hotel['description'],location[0])
                curr.execute("INSERT INTO hotels (name,address,distance,star_rating,description,location_id) "
                                "VALUES (?,?,?,?,?,?)", new_hotel)
                conn.commit()
                hotel_names.append(hotel['name'])
                hotel_addresses.append(hotel['address'])

        # We've found as many hotels as possible in this radius.
        if not new_hotels_found:
            radius += 5
            curr.execute("UPDATE destinations SET distance_tried = ? WHERE id = ?", (radius,location[0]))
            conn.commit()

        print(f"New hotels: {len(hotels)}")
        print(f"Current radius: {radius}")

    return (len(hotels),radius)

def populate_room_rates(hotel_id,location,model='8'):
    with sqlite3.connect('travel_data.db') as conn:
        curr = conn.cursor()
        
        curr.execute("SELECT id FROM room_rates WHERE hotel_id = ?",(hotel_id,))
        rows = curr.fetchall()

        # We've already populated room rates for this hotel.
        if len(rows) != 0:
            return
        
        curr = conn.cursor()
        curr.execute("SELECT id,name,address FROM hotels WHERE id = ?",(hotel_id,))
        rows = curr.fetchall()

        print(f"Populating room rates for {rows[0][1]} in {location[1]}")

        query = get_room_rate_query(location,rows[0][1],rows[0][2])
        room_rates = execute_llm_query(query,max_tokens = 1024,model=model)
        # The 8b context LLM seems to struggle with closing the list.
        # Thanks 8b model!
        if room_rates[-1] != ']':
            room_rates += ']'

        room_rates = ast.literal_eval(room_rates)
        for room_rate in room_rates:
            new_room_rate = (hotel_id,room_rate['room_type'],room_rate['room_description'],room_rate['winter_rate'],
                             room_rate['summer_rate'],room_rate['cancellation_policy'],str(room_rate['amenities']))
            curr.execute("INSERT INTO room_rates (hotel_id,room_type,room_description,winter_rate,summer_rate,"
                         "cancellation_policy,amenities) VALUES (?,?,?,?,?,?,?)", new_room_rate)
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
