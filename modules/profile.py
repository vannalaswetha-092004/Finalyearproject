import sqlite3

DB_PATH = "data/users.db"

def create_profile_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        username TEXT PRIMARY KEY,
        age INTEGER,
        height REAL,
        weight REAL,
        gender TEXT,
        goal TEXT,
        diseases TEXT,
        allergies TEXT
    )
    """)

    conn.commit()
    conn.close()

create_profile_table()

def save_profile(username, age, height, weight, gender, goal, diseases, allergies):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO profiles 
    VALUES (?,?,?,?,?,?,?,?)
    """, (username, age, height, weight, gender, goal, diseases, allergies))

    conn.commit()
    conn.close()

def get_profile(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profiles WHERE username=?", (username,))
    profile = cursor.fetchone()

    conn.close()
    return profile