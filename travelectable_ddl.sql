CREATE TABLE destinations(
id INTEGER PRIMARY KEY autoincrement,
location varchar,
country varchar,
latitude varchar,
longitude varchar,
description varchar,
points_of_interest varchar,
travel_advisory_level varchar(30));
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE hotels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        star_rating VARCHAR,
        address VARCHAR,
        distance VARCHAR,
        description VARCHAR,
        location_id INTEGER,
        FOREIGN KEY (location_id) REFERENCES destinations(id));
CREATE TABLE room_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_type VARCHAR,
        room_description VARCHAR,
        winter_rate INTEGER,
        summer_rate INTEGER,
        cancellation_policy VARCHAR,
        amenities VARCHAR,
        hotel_id INTEGER, image_id int references room_rate_images(id),
        FOREIGN KEY (hotel_id) REFERENCES hotels(id));
