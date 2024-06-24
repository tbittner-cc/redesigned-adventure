import concurrent.futures
import mock_data
import utilities
import sqlite3

locations = utilities.get_all_locations()

location = locations[0]

# open the database and get a cursor
with sqlite3.connect('travel_data.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT id FROM hotels WHERE location_id = ?", (location[0],))
    hotel_ids = curr.fetchall()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(mock_data.populate_room_rates,hotel_id[0],location) for hotel_id in hotel_ids]
    results = [future.result() for future in futures]
    