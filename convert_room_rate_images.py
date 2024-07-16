from io import BytesIO
import mock_data
from PIL import Image
import os
import sqlite3

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT id,room_type,image FROM room_rate_images")
    rows = curr.fetchall()

    for row in rows:
        loc_name = mock_data.return_room_rate_image_path(row[0],row[1])
        dir_path = f"images/room_rates"

        image = Image.open(BytesIO(row[2]))
        print(f"Saving...{dir_path}/{loc_name}.png")
        image.save(f"{dir_path}/{loc_name}.png")

    curr.execute("""SELECT rr.id,rri.id,rri.room_type from room_rates rr 
                    join room_rate_images rri on rr.id = rri.room_rate_id""")
