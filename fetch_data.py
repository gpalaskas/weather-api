# Imports
import requests
import os
import sqlite3
from dotenv import load_dotenv
from datetime import datetime, timedelta
from db import get_connection, init_db

# Meteomatics credentials
load_dotenv()
USERNAME = os.getenv("MY_USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Locations with latitude and longitude
locations = {
    "Athens": (37.9838, 23.7275),
    "Larnaca": (34.9229, 33.6233),
    "Thessaloniki": (40.6401, 22.9444)
}

# Date range (7 days)
start_date = datetime.now()
dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%SZ") for i in range(7)]

# Parameters to request from Meteomatics
parameter = "t_2m:C,absolute_humidity_2m:gm3"

# Get/create location ID in the database
def get_or_create_location_id(city, lat, lon):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM locations WHERE city = ?", (city,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO locations (city, latitude, longitude) VALUES (?, ?, ?)",
            (city, lat, lon)
        )
        conn.commit()
        return cursor.lastrowid

# Save a forecast record in the database
def save_forecast(location_id, forecast_date, temperature, humidity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO forecasts (location_id, forecast_date, temperature_c, humidity_gm3, fetched_at)
        VALUES (?, ?, ?,?, datetime('now'))
        """,
        (location_id, forecast_date, temperature, humidity)
    )
    conn.commit()

# Fetch weather data and store in DB 
def fetch_and_store_weather_data():
    init_db()
    for city, (lat, lon) in locations.items():
        location_id = get_or_create_location_id(city, lat, lon)
        print(f"\nGetting forecast for {city}...\n")

        for date in dates:
            url = f"https://api.meteomatics.com/{date}/{parameter}/{lat},{lon}/json"
            try:
                response = requests.get(url, auth=(USERNAME, PASSWORD))
                response.raise_for_status()
                data = response.json()

                temperature = None
                humidity = None
                for entry in data['data']:
                   if entry['parameter'] == 't_2m:C':
                      temperature = entry['coordinates'][0]['dates'][0]['value']
                   elif entry['parameter'] == 'absolute_humidity_2m:gm3':
                       humidity = entry['coordinates'][0]['dates'][0]['value']

                print(f"{date} -> Temp: {temperature} °C, Humidity: {humidity} gm3")
                save_forecast(location_id, date, temperature, humidity)

            except Exception as e:
                print(f"Failed to fetch data for {city} on {date}: {e}")

# Allow script to be run directly
if __name__ == "__main__":
    fetch_and_store_weather_data()