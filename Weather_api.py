import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from geopy.geocoders import Nominatim

# Function to get latitude and longitude from city/village name
def get_lat_lon(location_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        st.error("Could not find location. Please try another name.")
        return None, None

# Function to fetch weather data
def fetch_weather_data(latitude, longitude, start_date, end_date, hourly=False):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m" if hourly else None,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min" if not hourly else None,
        "timezone": "auto",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch weather data.")
        return None

# Streamlit UI
st.title("Weather Forecast App")
st.write("Get weather data for your city or village!")

# Input fields
location_name = st.text_input("Enter city or village name:")
date_range = st.date_input("Select Date Range", [])
data_type = st.selectbox("Select Data Type", ["Hourly Data", "Average Data"])

if st.button("Get Weather Data"):
    if location_name and len(date_range) == 2:
        start_date = date_range[0].strftime("%Y-%m-%d")
        end_date = date_range[1].strftime("%Y-%m-%d")

        latitude, longitude = get_lat_lon(location_name)
        if latitude and longitude:
            hourly = data_type == "Hourly Data"
            weather_data = fetch_weather_data(latitude, longitude, start_date, end_date, hourly=hourly)

            if weather_data:
                if hourly:
                    # Process hourly data
                    times = weather_data["hourly"]["time"]
                    temperatures = weather_data["hourly"]["temperature_2m"]
                    hourly_df = pd.DataFrame({"Time": times, "Temperature (°C)": temperatures})
                    st.write("Hourly Data:")
                    st.write(hourly_df)
                else:
                    # Process average data
                    max_temp = weather_data["daily"]["temperature_2m_max"]
                    min_temp = weather_data["daily"]["temperature_2m_min"]
                    dates = weather_data["daily"]["time"]
                    avg_temp = [(max_temp[i] + min_temp[i]) / 2 for i in range(len(dates))]
                    avg_df = pd.DataFrame({"Date": dates, "Average Temperature (°C)": avg_temp})
                    st.write(f"Average Data for {location_name}:")
                    st.write(avg_df)
    else:
        st.error("Please enter a location and select a valid date range.")
