import concurrent.futures
import mock_data
import sqlite3

def generate_hotel_images(hotel_id,name,description,location,country):
    mock_data.populate_hotel_images(hotel_id,name,description,location,country)
    
    with sqlite3.connect('travelectable.db') as conn:
        curr = conn.cursor()
        curr.execute("SELECT id FROM room_rates WHERE hotel_id = ?",(hotel_id,))  
        room_rate_id_tuples = curr.fetchall()
    for room_rate_id_tuple in room_rate_id_tuples:
        mock_data.populate_hotel_room_rate_images(room_rate_id_tuple[0])

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT id,location,country FROM destinations where id = 2")
    (location_id,location,country) = curr.fetchone()

    curr.execute(f"SELECT id,name,description FROM hotels where location_id = {location_id}")
    hotels = curr.fetchall()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(generate_hotel_images,hotel[0],hotel[1],hotel[2],location,country) 
                for hotel in hotels]
    results = [future.result() for future in futures]
