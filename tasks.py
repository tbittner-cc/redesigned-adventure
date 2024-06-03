import sqlite3
import replicate

from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

def get_all_locations():
    locations = []
    with sqlite3.connect('travel_data.db') as conn:
        curr = conn.cursor()
        curr.execute("SELECT id,location,city,state,country FROM destinations WHERE country = 'USA'")
        rows = curr.fetchall()
        for row in rows:
            if row[2] != '':
                locations.append((row[0],f"{row[2]}, {row[3]} {row[4]}"))
            else:
                locations.append((row[0],f"{row[1]}, {row[3]} {row[4]}"))

        curr.execute("SELECT id,location,country FROM destinations WHERE country != 'USA'")
        rows = curr.fetchall()
        for row in rows:
            locations.append((row[0],f"{row[1]}, {row[2]}"))

    return locations

locations = get_all_locations()[:10]

locations_groups = [locations[i:i+3] for i in range(0, len(locations), 3)]

print(locations_groups)

@app.task
def get_description_and_point_of_interest_data(location_group):
    for location in location_group:
        print(location[1])

for group in locations_groups:
    print_location.delay(group)
    