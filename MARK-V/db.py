import sqlite3
from datetime import datetime

conn = sqlite3.connect("neo_alpha.db", check_same_thread=False)
conn.execute("""CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY,
    time TEXT,
    who TEXT,
    message TEXT)""")

def save(who, message):
    conn.execute("INSERT INTO chats (time, who, message) VALUES (?,?,?)",
                 (datetime.now().isoformat(), who, message))
    conn.commit()

def search(word):
    return conn.execute(
        "SELECT time, who, message FROM chats WHERE message LIKE ? ORDER BY id DESC LIMIT 5",
        (f"%{word}%",)).fetchall()
