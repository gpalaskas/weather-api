--This is a copy of the the SQL queries that i use in main.py--

-- Query: List all locations
SELECT id, city, latitude, longitude FROM locations;

-- Query: Latest forecast per location and day
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

-- Query: Average of the last 3 forecasts per location/day
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

-- Query: Top-N cities by temperature or humidity
SELECT l.city, ROUND(AVG(f.temperature_c), 2) AS avg_temp
FROM forecasts f
JOIN locations l ON f.location_id = l.id
GROUP BY l.city
ORDER BY avg_temp DESC
LIMIT ?;
