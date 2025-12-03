import sqlite3, os, time
DB = "data/logs.db"
os.makedirs("data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS turns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        text TEXT,
        timestamp REAL
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        turn_id INTEGER,
        rating INTEGER,
        correction TEXT,
        timestamp REAL
    )""")
    conn.commit()
    conn.close()

def save_turn(session_id, role, text):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO turns (session_id, role, text, timestamp) VALUES (?, ?, ?, ?)",
              (session_id, role, text, time.time()))
    tid = c.lastrowid
    conn.commit(); conn.close()
    return tid

def save_feedback(turn_id, rating, correction=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO feedback (turn_id, rating, correction, timestamp) VALUES (?, ?, ?, ?)",
              (turn_id, rating, correction, time.time()))
    conn.commit(); conn.close()
