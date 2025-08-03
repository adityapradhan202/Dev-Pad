import sqlite3

conn = sqlite3.connect('devpad.db')
conn.execute("Create table Users (ID INT, NAME TEXT, USERNAME TEXT, PASS TEXT)")
print("Table successfully created!")
conn.close()

