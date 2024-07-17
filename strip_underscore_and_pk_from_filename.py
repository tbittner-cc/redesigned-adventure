import os

directory = "images/room_rates"

for filename in os.listdir(directory):
    index = filename.rfind("_")
    new_filename = filename[:index] + ".png"
    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
