import sqlite3

def connect():
    return sqlite3.connect("database.db", check_same_thread=False)

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER,
        age INTEGER,
        height REAL,
        weight REAL,
        gender TEXT,
        goal TEXT,
        diseases TEXT,
        allergies TEXT,
        beverages TEXT,
        meals_per_day INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_logs (
        user_id INTEGER,
        food_name TEXT,
        calories REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()