import mock_data
import utilities
import sqlite3

locations = utilities.get_all_locations()

los_angeles = locations[1]

with sqlite3.connect('travel_data.db') as conn:
  curr = conn.cursor()
  curr.execute("SELECT id FROM hotels WHERE location_id = ?", (los_angeles[0],))
  hotel_ids = curr.fetchall()

for hotel_id in hotel_ids:
  mock_data.populate_room_rates(hotel_id[0],los_angeles)