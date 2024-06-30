import sqlite3

with sqlite3.connect('travelectable.db') as conn:
    curr = conn.cursor()
    curr.execute("SELECT DISTINCT room_type FROM room_rates ORDER BY room_type")
    rows = curr.fetchall()
    print(f"Room Types: {len(rows)}")
    for row in rows:
        print(row[0])
