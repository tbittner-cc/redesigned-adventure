from PIL import Image
import mock_data
import sqlite3

image = Image.open('chicagoan_int.png')
img_stream = mock_data.create_scaled_bytestream(image)

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("INSERT INTO hotel_images (image,hotel_id) VALUES (?,?)",(img_stream,1))
    conn.commit()
