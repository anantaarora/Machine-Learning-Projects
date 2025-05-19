import requests
import pandas as pd
import os
from datetime import datetime, timedelta, timezone

def fetch_nasa_power_data(lat, lon, city_name):
    # Ensure the output directory exists
    output_dir = "solar_irradiance_data"
    os.makedirs(output_dir, exist_ok=True)

    # Get the current date and one year ago
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=365)
    
    # Format the start and end dates in the required format (YYYYMMDD)
    start_date_str = start_date.strftime('%Y%m%d')
    end_date_str = end_date.strftime('%Y%m%d')

    # API URL for UTC data (hourly, YTD)
    utc_url = (
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?start={start_date_str}&end={end_date_str}"
        f"&latitude={lat}&longitude={lon}&community=re&parameters=ALLSKY_SFC_SW_DWN,"
        "CLRSKY_SFC_SW_DWN,ALLSKY_SFC_SW_DIFF,T2M,WS10M,PS,SZA,SRF_ALB,RH2M,PRECTOTCORR"
        "&format=CSV&header=true&time-standard=UTC"
    )
    
    # Fetch data
    try:
        utc_response = requests.get(utc_url)
        utc_response.raise_for_status()  # Check for HTTP request errors
        utc_data = utc_response.content
        
        # Write UTC data to a temporary CSV file
        utc_file_path = os.path.join(output_dir, "nasa_power_utc.csv")
        with open(utc_file_path, "wb") as utc_file:
            utc_file.write(utc_data)
            
        print("Data successfully retrieved.")

        # Read the CSV file after skipping the first 18 rows and using the 19th row as the header
        utc_df = pd.read_csv(utc_file_path, skiprows=18)  # Skip first 18 rows (header starts from row 19)
        
        # Separate the UTC header (first 18 rows) and save as parameters.csv
        utc_header = pd.read_csv(utc_file_path, header=None, nrows=18)
        utc_header.to_csv(os.path.join(output_dir, f"nasa_power_parameters_{city_name}.csv"), index=False, header=False)

        # Combine the four columns into a single datetime column
        utc_df['date'] = pd.to_datetime(utc_df[['YEAR', 'MO', 'DY', 'HR']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')
        
        # Insert the new 'date' column at the first position (index 0)
        utc_df.insert(0, 'date', utc_df.pop('date'))
        
        # Save the merged dataframe to a new CSV file with dynamic naming
        output_filename_utc = os.path.join(output_dir, f"nasa_power_utc_{city_name}.csv")
        utc_df.to_csv(output_filename_utc, index=False)
        
        print(f"All data saved as {output_filename_utc}.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except pd.errors.ParserError as e:
        print(f"Error reading CSV data: {e}")

# Input from the user for latitude, longitude, and city name
if __name__ == "__main__":
    lat = float(input("Enter the latitude of the city: "))
    lon = float(input("Enter the longitude of the city: "))
    city_name = input("Enter the city name: ")

    # Fetch and process the data
    fetch_nasa_power_data(lat, lon, city_name)
