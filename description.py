import mock_data
import time
import utilities

from celery import Celery

app = Celery('description', broker='redis://localhost:6379/0')

locations = utilities.get_all_locations()

@app.task
def get_description_and_point_of_interest_data(locations):
    for location in locations:
        time.sleep(1)
        mock_data.populate_location_description_and_points_of_interest(location)

get_description_and_point_of_interest_data.delay(locations)
    