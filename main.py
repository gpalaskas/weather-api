from fastapi import FastAPI, Query
import sqlite3
from db import get_connection
from typing import List
from datetime import datetime
from models import LocationOut, LatestForecastOut, AverageTempOut, TopLocationOut
from fetch_data import fetch_and_store_weather_data  # Import fetch function

app = FastAPI()

# List all locations stored in the DB
@app.get("/locations", response_model=List[LocationOut])
def list_locations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, city, latitude, longitude FROM locations")
    rows = cursor.fetchall()
    return [{"id": row[0], "city": row[1], "lat": row[2], "lon": row[3]} for row in rows]

# Get latest forecast for each city and day
@app.get("/forecasts/latest", response_model=List[LatestForecastOut])
def latest_forecasts():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT l.city, DATE(f.forecast_date) as date, f.temperature_c, f.humidity_gm3
    FROM forecasts f
    JOIN locations l ON l.id = f.location_id
    WHERE f.fetched_at IN (
        SELECT MAX(f2.fetched_at)
        FROM forecasts f2
        WHERE DATE(f2.forecast_date) = DATE(f.forecast_date)
        AND f2.location_id = f.location_id
    )
    ORDER BY l.city, date;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    return [
        {"city": row[0], "date": row[1], "temperature": round(row[2], 2), "humidity": row[3]} for row in rows
    ]

# Get average of last 3 temperature forecasts per city per day
@app.get("/forecasts/average-temp", response_model=List[AverageTempOut])
def average_temp():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    WITH ranked_forecasts AS (
        SELECT
            l.city,
            DATE(f.forecast_date) AS date,
            f.temperature_c,
            f.fetched_at,
            ROW_NUMBER() OVER (
                PARTITION BY f.location_id, DATE(f.forecast_date)
                ORDER BY f.fetched_at DESC
            ) AS row_num
        FROM forecasts f
        JOIN locations l ON f.location_id = l.id
    )
    SELECT
        city,
        date,
        ROUND(AVG(temperature_c), 2) AS avg_temperature
    FROM ranked_forecasts
    WHERE row_num <= 3
    GROUP BY city, date
    ORDER BY city, date;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    return [
        {"city": row[0], "date": row[1], "avg_temperature": row[2]} for row in rows
    ]

# Get top-n locations based on a given metric (temperature or humidity)
@app.get("/locations/top-n", response_model=List[TopLocationOut])
def top_n_locations(n: int, metric: str = "temperature"):
    conn = get_connection()
    cursor = conn.cursor()
    metric_column_map = {
        "temperature": "temperature_c",
        "humidity": "humidity_gm3"
    }
    if metric not in metric_column_map:
        return {"error": "Invalid metric. Choose 'temperature' or 'humidity'."}

    selected_column = metric_column_map[metric]
    query = f"""
    SELECT l.city, ROUND(AVG(f.{selected_column}), 2) AS avg_metric
    FROM forecasts f
    JOIN locations l ON f.location_id = l.id
    GROUP BY l.city
    ORDER BY avg_metric DESC
    LIMIT ?
    """
    cursor.execute(query, (n,))
    rows = cursor.fetchall()
    return [
        {"city": row[0], "avg_metric": row[1]} for row in rows
    ]

# Endpoint to trigger data refresh manually or via cron job
@app.post("/refresh")
def refresh_data():
    fetch_and_store_weather_data()
    return {"message": "Weather data updated successfully"}