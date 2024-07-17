from io import BytesIO
import mock_data
from PIL import Image
import os
import sqlite3

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT DISTINCT room_type FROM room_rates ORDER BY room_type")
    rows = curr.fetchall()

    uniq_images = []
    for row in rows:
        loc_name = mock_data.return_room_rate_image_path(row[0])
        dir_path = f"images/room_rates"

        if not os.path.exists(f"{dir_path}/{loc_name}.png"):
            uniq_images.append(row[0])

print (len (uniq_images))
