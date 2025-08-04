# This script is for testing purpose only
# Run this script to create a database devpad.db with table posts
import sqlite3

conn = sqlite3.connect('devpad.db')
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL)
    """)

cur.close()
conn.close()

