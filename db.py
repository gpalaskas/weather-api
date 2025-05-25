import sqlite3

def get_connection():
    return sqlite3.connect("weather.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create locations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT UNIQUE NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        );
    """)

    # Create forecasts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            forecast_date TEXT,
            temperature_c REAL,
            humidity_gm3 REAL,
            fetched_at TEXT,
            FOREIGN KEY (location_id) REFERENCES locations(id)
        );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")