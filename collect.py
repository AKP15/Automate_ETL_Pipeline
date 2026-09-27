import logging
import requests
import pandas as pd
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

CITIES = [
    {"name": "Yangon", "latitude": 16.866, "longitude": 96.195},
    {"name": "Mandalay", "latitude": 21.958, "longitude": 96.089},
    {"name": "Naypyidaw", "latitude": 19.763, "longitude": 96.078},
    {"name": "Bago", "latitude": 17.336, "longitude": 96.479},
    {"name": "Mawlamyine", "latitude": 16.491, "longitude": 97.625},
    {"name": "Sittwe", "latitude": 20.153, "longitude": 92.899},
    {"name": "Monywa", "latitude": 22.109, "longitude": 95.136},
    {"name": "Meiktila", "latitude": 20.882, "longitude": 95.858},
    {"name": "Taunggyi", "latitude": 20.782, "longitude": 97.039},
    {"name": "Pathein", "latitude": 16.779, "longitude": 94.732},
]

API_URL = "https://api.open-meteo.com/v1/forecast"
OUTPUT_FILE = "city_weather.csv"


def extract(city: dict) -> dict | None:
    """Call the Open-Meteo API for one city and return the raw JSON, or None on failure."""
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "current_weather": "true",
    }
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data for {city['name']}: {e}")
        return None


def transform(city: dict, raw_data: dict) -> pd.DataFrame:
    """Turn one city's raw API response into a single-row DataFrame."""
    current = raw_data["current_weather"]
    now = datetime.now()

    return pd.DataFrame({
        "Date": [now.strftime("%Y-%m-%d")],
        "Time": [now.strftime("%H:%M:%S")],
        "City": [city["name"]],
        "Latitude": [city["latitude"]],
        "Longitude": [city["longitude"]],
        "Temperature (C)": [current["temperature"]],
        "Wind Speed (km/h)": [current["windspeed"]],
        "Wind Direction (deg)": [current["winddirection"]],
    })


def load(df: pd.DataFrame, file_name: str = OUTPUT_FILE) -> None:
    """Append a row to the CSV, writing the header only if the file doesn't exist yet."""
    write_header = not os.path.exists(file_name)
    df.to_csv(file_name, mode="a", index=False, header=write_header)


def city_weather_collector():
    """Run one full extract -> transform -> load cycle for every city."""
    for city in CITIES:
        raw_data = extract(city)
        if raw_data is None:
            continue  # skip this city, keep going with the rest

        try:
            df = transform(city, raw_data)
            load(df)
            logging.info(f"Collected weather for {city['name']}")
        except (KeyError, TypeError) as e:
            logging.error(f"Unexpected response shape for {city['name']}: {e}")
