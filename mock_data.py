import ast
from io import BytesIO
from PIL import Image
import os
import replicate
import requests
import sqlite3

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

def get_location_image_query(location,country):
    return f"""
    Provide a tourist-friendly image of {location} {country}.
    """

def get_hotel_image_query(name,description,location,country,exterior = True):
    if exterior:
        descriptor = "exterior of the building"
    else:
        descriptor = "interior, common area like a lobby, bar, etc."
    return f"""
    For the hotel '{name}' in {location}, {country} described as 
    
    {description} 
    
    provide an {descriptor} image.
    """

def get_room_rate_image_query(room_type):
    return f"""
    A photo-realistic {room_type} hotel room type taken from the perspective of being in the room.
    """

def execute_llm_query(query,max_tokens = 512,model='70'):
    data = replicate.run(
        f"meta/meta-llama-3-{model}b-instruct",
         input={"prompt": query, "max_tokens": max_tokens})

    return "".join(data)

def execute_image_query(query):
    output = replicate.run(
    "bytedance/sdxl-lightning-4step:5f24084160c9089501c1b3545d9be3c27883ae2239b6f412990e82d4a6210f8f",
    input={
        "width": 1024,
        "height": 1024,
        "prompt": query,
        "scheduler": "K_EULER",
        "num_outputs": 1,
        "guidance_scale": 0,
        "negative_prompt": "worst quality, low quality",
        "num_inference_steps": 4
    })

    response = requests.get(output[0])
    image = Image.open(BytesIO(response.content))

    return image


def create_scaled_bytestream(image,image_fomat='PNG'):
    width, height = image.size
    resized_image = image.resize((width // 3, height // 3))
    image_byte_stream = BytesIO()
    resized_image.save(image_byte_stream, format=image_fomat)
    image_bytes = image_byte_stream.getvalue()

    return image_bytes

def return_location_image_path(location_id,location_name):
    file_path = location_name.replace(' ','_').replace('.','').lower()
    return f"""{file_path}_{location_id}"""

def return_hotel_image_path(hotel_id,hotel_name):
    file_path = hotel_name.replace(' ','_').replace('.','').replace('\'','').lower()
    return f"""{file_path}_{hotel_id}"""

def return_room_rate_image_path(room_type):
    file_path = room_type.replace(' ','_').replace('.','').replace('\'','').lower()
    return file_path

def update_location_description_and_points_of_interest(location,country,model='70'):
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

        retries = 0
        while retries < 3:
            try:
                query = get_hotel_query_v2(location,country)
                hotels = execute_llm_query(query,max_tokens = 1536,model=model)
                hotels = ast.literal_eval(hotels)
                break
            except Exception as e:
                print(e)
                retries += 1

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

        print(f"Populating room rates for {hotel_name} in {location}, {country}")
        
        retries = 0
        while retries < 3:
            try:
                query = get_room_rate_query_v2(location,country,hotel_name,description)
                room_rates = execute_llm_query(query,max_tokens = 1024,model=model)
                room_rates = ast.literal_eval(room_rates)
                break
            except Exception as e:
                print(e)
                retries += 1

        with sqlite3.connect('travelectable.db') as conn:
            curr = conn.cursor()
            for room_rate in room_rates:
                new_room_rate = (hotel_id,room_rate['room_type'],room_rate['room_description'],room_rate['winter_rate'],
                                 room_rate['summer_rate'],room_rate['cancellation_policy'],str(room_rate['amenities']))
                curr.execute("INSERT INTO room_rates (hotel_id,room_type,room_description,winter_rate,summer_rate,"
                             "cancellation_policy,amenities) VALUES (?,?,?,?,?,?,?)", new_room_rate)
                conn.commit()

def populate_location_image(location_id):
    with sqlite3.connect('travelectable.db') as conn:
        curr = conn.cursor()

        curr.execute("SELECT location,country,image FROM destinations WHERE id = ?",(location_id,))
        rows = curr.fetchone()

        # We've already populated the image for this location.
        if rows[2] is not None:
            return

        print(f"Populating location images for {rows[0]}, {rows[1]}")

        query = get_location_image_query(rows[0],rows[1])
        image = execute_image_query(query)
        stream = create_scaled_bytestream(image)

        curr.execute("UPDATE destinations SET image = ? WHERE id = ?",(stream,location_id))
        conn.commit()

def populate_hotel_images(hotel_id,name,description,location_id,location,country):
    with sqlite3.connect('travelectable.db') as conn:
        curr = conn.cursor()
        curr.execute("SELECT count(id) FROM hotel_images WHERE hotel_id = ?",(hotel_id,))
        count = curr.fetchone()[0]

        if count > 0:
            return

        print(f"Populating hotel images for {name} in {location}, {country}")

        query = get_hotel_image_query(name,description,location,country,exterior = True)
        exterior_image = execute_image_query(query)
        ext_stream = create_scaled_bytestream(exterior_image)

        query = get_hotel_image_query(name,description,location,country,exterior = False)
        interior_image = execute_image_query(query)
        int_stream = create_scaled_bytestream(interior_image)

        loc_name = return_location_image_path(location_id,location)
        hot_name = return_hotel_image_path(hotel_id,name)
        dir_path = f"images/{loc_name}/{hot_name}"

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)  

        image = Image.open(BytesIO(ext_stream))
        full_path = f"{dir_path}/ext_{hotel_id}.png"
        image.save(full_path)
        curr.execute("INSERT INTO hotel_images (image_path,hotel_id,is_lead_image) VALUES (?,?,?)",
                     (full_path,hotel_id,True))
            
        image = Image.open(BytesIO(int_stream))
        full_path = f"{dir_path}/int_{hotel_id}.png"
        image.save(full_path)
        curr.execute("INSERT INTO hotel_images (image_path,hotel_id,is_lead_image) VALUES (?,?,?)",
                     (full_path,hotel_id,False))
        conn.commit()

def populate_hotel_room_rate_images(room_type):
        room_name = return_room_rate_image_path(room_type)
        file_path = f"images/room_rates/{room_name}.png"

        if os.path.exists(file_path):
            return

        print(f"Populating room rate images for {room_type} room rate")

        query = get_room_rate_image_query(room_type)
        image = execute_image_query(query)
        stream = create_scaled_bytestream(image)

        image = Image.open(BytesIO(stream))
        image.save(file_path)
