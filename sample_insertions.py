# Run this script to insert some data into the database
# This script is also for testing puprose
import sqlite3

conn = sqlite3.connect("devpad.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("INSERT INTO posts (content) VALUES (?)", ("Hello my name is aditya",))
cur.execute("INSERT INTO posts (content) VALUES (?)", ("Mujhe sydney sweeny ki kachi khaani hai",))
cur.execute("INSERT INTO posts (content) VALUES (?)", ("Python is dope!",))

cur.execute("SELECT * FROM posts")
rows = cur.fetchall()
for row in rows:
    print(row["id"])
    print(row["content"])

conn.commit()
cur.close()
conn.close()