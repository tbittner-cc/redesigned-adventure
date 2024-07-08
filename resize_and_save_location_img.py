import os
from PIL import Image

# Open an image file
image = Image.open("chicago_original.jpg")

# Get the width and height of the image
width, height = image.size

print(f"Width: {width}, Height: {height}")
print("Width-to-height ratio: {:.2f}".format(width / height))

size_in_bytes = os.path.getsize("chicago_original.jpg")

size_in_mb = size_in_bytes / (1024 * 1024)

print(f"Size in MB: {size_in_mb:.2f}MB")

resized_image = image.resize((width // 5,int(width // 5*(height/width))))

resized_image.save("chicago_resized.jpg")

width, height = resized_image.size

print(f"Width: {width}, Height: {height}")
print("Width-to-height ratio: {:.2f}".format(width / height))

size_in_bytes = os.path.getsize("chicago_resized.jpg")

size_in_mb = size_in_bytes / (1024 * 1024)

print(f"Size in MB: {size_in_mb:.2f}MB")