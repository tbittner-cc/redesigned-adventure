import concurrent.futures
import mock_data
import sqlite3

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT id,location,country FROM destinations")
    rows = curr.fetchall()

location_lists = [rows[i:i+10] for i in range(0,len(rows),10)]

for location_list in location_lists:
    for location in location_list:
        with sqlite3.connect('travelectable.db') as conn:
            curr = conn.cursor()
            curr.execute("SELECT id,name,description FROM hotels WHERE location_id = ?", (location[0],))
            hotels = curr.fetchall()
        
        for hotel in hotels:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(mock_data.populate_room_rates_v2,hotel[0],location[1],location[2],
                                             hotel[1],hotel[2],model='70')
                           for hotel in hotels]
                results = [future.result() for future in futures]
