from io import BytesIO
from PIL import Image
import os
import sqlite3

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT id,location,country,image FROM destinations")
    rows = curr.fetchall()

    for row in rows:
        loc_name = row[1].replace(' ','_').replace('.','').lower()
        dir_path = f"images/{loc_name}_{row[0]}"
        print(dir_path)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        image = Image.open(BytesIO(row[3]))
        image.save(f"{dir_path}/{loc_name}_{row[0]}.png")

    curr.execute("ALTER TABLE destinations DROP COLUMN image")
    curr.execute("ALTER TABLE destinations ADD COLUMN image_path varchar")    
    conn.commit()

    for row in rows:
        curr.execute("UPDATE destinations SET image_path = ? WHERE id = ?",
            (f"/images/{loc_name}_{row[0]}/{loc_name}_{row[0]}.png",row[0]))
    conn.commit()
