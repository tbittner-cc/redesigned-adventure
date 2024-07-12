from io import BytesIO
import mock_data
from PIL import Image
import os
import sqlite3

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT id,image,hotel_id,is_lead_image FROM hotel_images") 
    img_rows = curr.fetchall()

    for img_row in img_rows:
        curr.execute("""SELECT d.id,d.location,h.id,h.name FROM destinations d join hotels h on d.id = h.location_id 
                        WHERE h.id = ?""",(img_row[2],))
        loc_rows = curr.fetchall()

        for loc_row in loc_rows:
            loc_name = mock_data.return_location_image_path(loc_row[0],loc_row[1])
            hot_name = mock_data.return_hotel_image_path(loc_row[2],loc_row[3])
            dir_path = f"images/{loc_name}/{hot_name}"

            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            image = Image.open(BytesIO(img_row[1]))
            if img_row[3] == 1:
                img_name = f"{dir_path}/ext_{img_row[0]}.png"
            else:
                img_name = f"{dir_path}/int_{img_row[0]}.png"
            
            image.save(img_name)

            curr.execute("UPDATE hotel_images SET image_path = ? WHERE id = ?",(f"{img_name}",img_row[0]))

    conn.commit()

    # for loc_row in loc_rows:
    #     loc_name = mock_data.return_location_image_path(loc_row[0],loc_row[1])
    #     curr.execute("SELECT id,name FROM hotels WHERE location_id = ?",(loc_row[0],))
    #     hot_rows = curr.fetchall()
        
    #     for hot_row in hot_rows:
    #         hot_name = mock_data.return_hotel_image_path(hot_row[0],hot_row[1])
    #         dir_path = f"images/{loc_name}/{hot_name}"
    #         print(dir_path)
    #         if not os.path.exists(dir_path):
    #             os.mkdir(dir_path)

            #image = Image.open(BytesIO(hot_row[0]))
            #image.save(f"{dir_path}/{hot_name}_{hot_row[0]}.png")

    # for row in rows:
    #     loc_name = row[1].replace(' ','_').replace('.','').lower()
    #     dir_path = f"images/{loc_name}_{row[0]}"
    #     print(dir_path)
    #     if not os.path.exists(dir_path):
    #         os.mkdir(dir_path)

    #     image = Image.open(BytesIO(row[3]))
    #     image.save(f"{dir_path}/{loc_name}_{row[0]}.png")

    # curr.execute("ALTER TABLE hotels DROP COLUMN image")
    # curr.execute("ALTER TABLE hotels ADD COLUMN image_path varchar")    
    # conn.commit()

    # for row in rows:
    #     curr.execute("UPDATE hotels SET image_path = ? WHERE id = ?",
    #         (f"/images/{loc_name}_{row[0]}/{loc_name}_{row[0]}.png",row[0]))
    # conn.commit()