import sqlite3

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
