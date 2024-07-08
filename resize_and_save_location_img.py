from io import BytesIO
import os
import argparse
from PIL import Image
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument("file_name", type=str)
parser.add_argument("location_id", type=int)
args = parser.parse_args()

# Open an image file
image = Image.open(args.file_name)

# Get the width and height of the image
width, height = image.size

print(f"Width: {width}, Height: {height}")
print("Width-to-height ratio: {:.2f}".format(width / height))

resized_image = image.resize((width // 5, height // 5))
img_byte_stream = BytesIO()

resized_image.save(img_byte_stream, format="JPEG")

image_bytes = img_byte_stream.getvalue()

# new_image = Image.open(BytesIO(image_bytes))
# new_image.show()

# r_img_bytes = resized_image.tobytes()
# new_image = Image.frombytes(resized_image.mode, resized_image.size, r_img_bytes)
# new_image.show()

with sqlite3.connect('travelectable.db') as conn:
     curr = conn.cursor()
     curr.execute("UPDATE destinations SET image = ? WHERE id = ?", (sqlite3.Binary(image_bytes), args.location_id))
     conn.commit()

with sqlite3.connect('travelectable.db') as conn:
     curr = conn.cursor()
     curr.execute("SELECT image FROM destinations WHERE id = ?", (args.location_id,))
     rows = curr.fetchone()
     image = rows[0]
     image = Image.open(BytesIO(image))
     image.show()