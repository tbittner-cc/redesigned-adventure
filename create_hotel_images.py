import concurrent.futures
import mock_data
import sqlite3

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT id FROM destinations ORDER BY id")
    rows = curr.fetchall()

location_ids = [row[0] for row in rows]

location_ids = location_ids[0:30]

for location_id in location_ids:
    with sqlite3.connect('travelectable.db') as conn:
        curr = conn.cursor()
        curr.execute("SELECT id,location,country FROM destinations where id = ?",(location_id,))
        (location_id,location,country) = curr.fetchone()

        curr.execute(f"SELECT id,name,description FROM hotels where location_id = {location_id}")
        hotels = curr.fetchall()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(mock_data.populate_hotel_images,hotel[0],hotel[1],hotel[2],location_id,location,country) 
                    for hotel in hotels]
        results = [future.result() for future in futures]
