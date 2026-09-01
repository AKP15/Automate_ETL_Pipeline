import requests
import pandas as pd
from datetime import datetime
import os

def city_wealther_collector():
    url = "https://api.open-meteo.com/v1/forecast"
    cities = [
        {"name": "Yangon", "latitude": 16.866, "longitude": 96.195},
        {"name": "Mandalay", "latitude": 21.958, "longitude": 96.089},
        {"name": "Naypyidaw", "latitude": 19.763, "longitude": 96.078},
        {"name": "Bago", "latitude": 17.336, "longitude": 96.479},
        {"name": "Mawlamyine", "latitude": 16.491, "longitude": 97.625},
        {"name": "Sittwe", "latitude": 20.153, "longitude": 92.899},
        {"name": "Monywa", "latitude": 22.109, "longitude": 95.136},
        {"name": "Meiktila", "latitude": 20.882, "longitude": 95.858},
        {"name": "Taunggyi", "latitude": 20.782, "longitude": 97.039},
        {"name": "Pathein", "latitude": 16.779, "longitude": 94.732}
                                                   ]

    for city in cities:
        params={
            "latitude": city['latitude'], 
            "longitude": city['longitude'],
            "current_weather":"true"
            }
        response=requests.get(url,params=params)
        if response.status_code == 200:
            print("Success")
        else:
            print(response.status_code)
        data=response.json()
        current_temp = data["current_weather"]["temperature"]
        wind_speed = data["current_weather"]["windspeed"]
        wind_direction = data["current_weather"]["winddirection"]
        date = datetime.now().strftime("%Y-%m-%d ")
        time  = datetime.now().strftime("%H:%M:%S")
        df = pd.DataFrame({
                "Date":[date],
                "Time": [time],
                "Airport": [city["name"]],
                "Latitude": [city["latitude"]],
                "Longitude": [city["longitude"]],
                "Temperature (C)": [current_temp],
                "Wind Speed (km/h)": [wind_speed]
                                    })
        file_name = "city_weather.csv"
        if os.path.exists(file_name):
            write_header = False
        else:
            write_header = True
        df.to_csv(file_name, mode="a", index=False, header=write_header)
        
