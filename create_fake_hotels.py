import concurrent.futures
import mock_data
import sqlite3


with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT id,location,country FROM destinations")
    rows = curr.fetchall()

location_lists = [rows[i+1:i+10] for i in range(0,len(rows),10)]

for location_list in location_lists:
    for row in location_list:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(mock_data.populate_hotels_v2,row[0],row[1],row[2],model='70') 
                       for row in location_list]
            results = [future.result() for future in futures]
