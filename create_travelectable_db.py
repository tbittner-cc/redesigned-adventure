import sqlite3

# Connect to the database
conn = sqlite3.connect('travelectable.db')
c = conn.cursor()

c.execute('''
SELECT name FROM sqlite_master WHERE type='table' AND name='destinations'
''')

if not c.fetchone():
    c.execute('''   
    CREATE TABLE destinations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location VARCHAR,
        country VARCHAR,
        latitude VARCHAR,
        longitude VARCHAR,
        description VARCHAR,
        points_of_interest VARCHAR,
        travel_advisory_level VARCHAR
        image_url VARCHAR);
    ''')

c.execute('''
SELECT name FROM sqlite_master WHERE type='table' AND name='hotels'
''')

if not c.fetchone():
    c.execute('''
    CREATE TABLE hotels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        star_rating VARCHAR,
        address VARCHAR,
        distance VARCHAR,
        description VARCHAR,
        location_id INTEGER,
        FOREIGN KEY (location_id) REFERENCES destinations(id));
    ''')

c.execute('''
SELECT name FROM sqlite_master WHERE type='table' AND name='room_rates'
''')

if not c.fetchone():
    c.execute('''
    CREATE TABLE room_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_type VARCHAR,
        room_description VARCHAR,
        winter_rate INTEGER,
        summer_rate INTEGER,
        cancellation_policy VARCHAR,
        amenities VARCHAR,
        image BLOB,
        hotel_id INTEGER,
        FOREIGN KEY (hotel_id) REFERENCES hotels(id));
    ''')

c.execute('''
SELECT name FROM sqlite_master WHERE type='table' AND name='hotel_images'
''')

if not c.fetchone():
    c.execute('''
    CREATE TABLE hotel_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image BLOB,
        hotel_id INTEGER,
        FOREIGN KEY (hotel_id) REFERENCES hotels(id));
    ''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
