import sqlite3


with sqlite3.connect('travel_data.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT location FROM destinations")
    locations = curr.fetchall()

for location in locations:
    print(location[0])