import sqlite3

def db_initialize():
    conn = sqlite3.connect("devpad.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL)
    """)
    return cur, conn

# To fetch all the posts
def fetchall_posts(cur, conn):
    cur.execute("SELECT * FROM posts")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows

# To delete rows
def delete_posts(cur, conn, pid):
    cur.execute("DELETE FROM posts WHERE ID=?", (pid,))
    conn.commit()
    cur.close()
    conn.close()

def get_single_post(cur, conn, pid):
    cur.execute("SELECT * FROM posts WHERE ID=?", (pid,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return row


if __name__ == "__main__":
    # Testing here
    cur, conn = db_initialize()
    rows = fetchall_posts(cur, conn)
    print(rows)
