# Importing the packages to make the calls and manipulate the resulting files
import requests
from datetime import datetime, timedelta, timezone
import pandas as pd
import os

# Defining the API key to make the calls
api_key = '555863aca3fca425f071a11409e86a82'

def fetch_weather_data(lat, lon, city_name):
    # Get the current date and one year ago
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=365)

    # Convert start_date to a Unix timestamp
    start_date_unix = int(start_date.timestamp())

    base_url = "https://history.openweathermap.org/data/2.5/history/city"
    type_param = "hour"
    units_param = "metric"
    app_id_param = api_key
    
    data = {'list': []}
    print("Please wait.....")
    
    for i in range(52):
        start_timestamp = int(start_date_unix) + i * 604800
        end_timestamp = int(start_timestamp) + 604800 - 3600  # Subtract one hour
        
        weather_data_url = f"{base_url}?lat={lat}&lon={lon}&type={type_param}&start={start_timestamp}&end={end_timestamp}&units={units_param}&appid={app_id_param}"
        get_weather_data = requests.get(weather_data_url)
        new_data = get_weather_data.json()
        
        # Avoid errors if 'list' is missing
        if 'list' in new_data:
            data['list'].extend(new_data['list'])
    
    print(f"Total data points fetched: {len(data['list'])}")
    
    transformed_data_list = []
    
    for entry in data['list']:
        date_time = datetime.utcfromtimestamp(entry["dt"]) - timedelta(hours=8)  # Adjust timezone if necessary
        
        # Safely access each key with .get() to avoid KeyErrors
        temperature = entry["main"].get("temp", -999)
        feels_like = entry["main"].get("feels_like", -999)
        pressure = entry["main"].get("pressure", -999)
        humidity = entry["main"].get("humidity", -999)
        temp_min = entry["main"].get("temp_min", -999)
        temp_max = entry["main"].get("temp_max", -999)
        speed = entry["wind"].get("speed", -999)
        deg = entry["wind"].get("deg", -999)
        clouds_all = entry["clouds"].get("all", -999)
        weather_id = entry["weather"][0].get("id", -999)
        weather_main = entry["weather"][0].get("main", -999)
        weather_description = entry["weather"][0].get("description", -999)
        weather_icon = entry["weather"][0].get("icon", -999)
        rain_1h = entry.get("rain", {}).get("1h", -999)
        
        transformed_data = {
            "Date": date_time,
            "Temperature": temperature,
            "Feels like": feels_like,
            "Pressure": pressure,
            "Humidity": humidity,
            "Minimum Temp (F)": temp_min,
            "Maximum Temp (F)": temp_max,
            "Wind Speed": speed,
            "Wind Degree": deg,
            "Rain 1h": rain_1h,
            "Clouds All": clouds_all,
            "Weather Id": weather_id,
            "Weather Main": weather_main,
            "Weather Description": weather_description,
            "Weather Icon": weather_icon
        }

        transformed_data_list.append(transformed_data)

    print("Data transformation successful.")

    df_data = pd.DataFrame(transformed_data_list)
    
    # Ensure the output directory exists
    output_directory = "weather_data"
    os.makedirs(output_directory, exist_ok=True)
    
    output_filename_weather = os.path.join(output_directory, f"openweather_data_{city_name}.csv")
    df_data.to_csv(output_filename_weather, index=False)
    print(f"Data saved to {output_filename_weather}")

if __name__ == '__main__':
    lat = float(input("Enter latitude: "))
    lon = float(input("Enter longitude: "))
    city_name = input("Enter city name (use underscores, no spaces): ")
    fetch_weather_data(lat, lon, city_name)
