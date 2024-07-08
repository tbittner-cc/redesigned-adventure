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
image_bytes = image.tobytes()

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("UPDATE destinations set image = ? WHERE id = ?", 
        (sqlite3.Binary(image_bytes),args.location_id))
    conn.commit()
    #image = curr.fetchone()[0]
    #image = Image.open(BytesIO(image))
    #image.save(f"{args.location_id}.png")