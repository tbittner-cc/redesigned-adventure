import concurrent.futures
import mock_data
import utilities

def get_hotel_for_location(location):
  len_hotels = 0
  radius = 0

  retries = 0
  result = ''
  while len_hotels < 40 and radius < 25:
    if retries > 15:
      print(f"Reached max retries for {location[1]}")
      break
    try:
      result = mock_data.populate_hotels(location)
      if result is None:
        break
      retries = 0
      len_hotels = result[0]
      radius = result[1]
    except Exception as e:
      print(e)
      retries += 1

locations = utilities.get_all_locations()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
  futures = [executor.submit(get_hotel_for_location,location) for location in locations]
  results = [future.result() for future in futures]
    