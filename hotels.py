import mock_data
import utilities

locations = utilities.get_all_locations()

los_angeles = locations[1]

len_hotels = 0
radius = 0

while len_hotels < 40 and radius < 25:
  result = mock_data.populate_hotels(los_angeles)
  len_hotels = result[0]
  radius = result[1]