import concurrent.futures
import sqlite3
import mock_data

# This was another legacy script that was used to populate descriptions and points of interest for mis-configured data.
with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT location,country FROM destinations")
    rows = curr.fetchall()

# Grab all the rows that were populating descriptions from a None location.
rows = rows[20:43]

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
  futures = [executor.submit(mock_data.update_location_description_and_points_of_interest,row[0],row[1],model='70') 
              for row in rows]
  results = [future.result() for future in futures]
