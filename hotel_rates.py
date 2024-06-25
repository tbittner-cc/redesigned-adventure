import concurrent.futures
import mock_data
import utilities
import sqlite3

locations = utilities.get_all_locations()

def get_rates_for_hotel(hotel_id,location):
    retries = 0

    while retries < 5:
        try:
            mock_data.populate_room_rates(hotel_id,location)
            break
        except Exception as e:
            print(e)
            retries += 1
    if retries >= 5:
        # Try once with the greater context LLM
        mock_data.populate_room_rates(hotel_id,location,'70')

for location in locations:
    # open the database and get a cursor
    with sqlite3.connect('travel_data.db') as conn:
        curr = conn.cursor()
        curr.execute("SELECT id FROM hotels WHERE location_id = ?", (location[0],))
        hotel_ids = curr.fetchall()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_rates_for_hotel,hotel_id[0],location) for hotel_id in hotel_ids]
        results = [future.result() for future in futures]
