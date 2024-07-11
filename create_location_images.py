import concurrent.futures
import mock_data
import sqlite3

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT id FROM destinations ORDER BY id")
    rows = curr.fetchall()

location_ids = [row[0] for row in rows]

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(mock_data.populate_location_image,location_id) 
                for location_id in location_ids]
    results = [future.result() for future in futures]
