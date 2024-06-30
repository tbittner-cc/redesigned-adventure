import ast
import sqlite3


with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT id,description,points_of_interest FROM destinations")
    data = curr.fetchall()

    for row in data:
        if '[' in row[1]:
            description = row[1].strip().strip('[')
            curr.execute("UPDATE destinations SET description = ? WHERE id = ?", (description,row[0]))
        landmarks = ast.literal_eval(row[2])
        landmarks = [landmark.strip() for landmark in landmarks]
        curr.execute("UPDATE destinations SET points_of_interest = ? WHERE id = ?", (str(landmarks),row[0]))
