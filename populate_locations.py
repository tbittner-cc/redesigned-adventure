import sqlite3

with open('locations.txt') as f:
    locations = f.read().splitlines()
print(len(locations))
locations_str = ','.join([f"'{location}'" for location in locations])

with sqlite3.connect('travel_data.db') as conn:
    curr = conn.cursor()
    curr.execute(f"Select location,city,country,latitude,longitude,description,points_of_interest,travel_advisory_level from destinations where location in ({locations_str})")
    rows = curr.fetchall()

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    for row in rows:
        row = list(row)
        if row[1] == '' or row[1] is None:
            del row[1]
        else:

            del row[0]
        curr.execute("Insert into destinations (location,country,latitude,longitude,description,points_of_interest,travel_advisory_level) values (?,?,?,?,?,?,?)", 
                     row)
