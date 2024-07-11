CREATE TABLE destinations(
id INTEGER PRIMARY KEY autoincrement,
location varchar,
country varchar,
latitude varchar,
longitude varchar,
description varchar,
points_of_interest varchar,
travel_advisory_level varchar(30), image blob);
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
CREATE TABLE hotel_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image BLOB,
        hotel_id INTEGER, is_lead_image BOOLEAN,
        FOREIGN KEY (hotel_id) REFERENCES hotels(id));
CREATE TABLE room_rate_images (
id integer primary key autoincrement,
room_type varchar,
image blob);
