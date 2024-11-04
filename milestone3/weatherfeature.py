import streamlit as st
import requests
import openai
from datetime import datetime
from collections import defaultdict

# Set your API keys here
OPENWEATHER_API_KEY = 'Weather_API_KEY'  # OpenWeather API key
OPENAI_API_KEY = 'OPEN_API_KEY'  # Replace with your actual OpenAI API key

# Function to fetch weather forecast from OpenWeather
def get_weather_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=imperial&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching weather data. Check the city name or your API key.")
        return None

# Function to calculate daily highs, lows, and total precipitation
def process_forecast_data(weather_data):
    daily_data = defaultdict(lambda: {"high": float('-inf'), "low": float('inf'), "precipitation_sum": 0})

    for entry in weather_data['list']:
        date_str = entry['dt_txt']
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
        temp = entry['main']['temp']
        precipitation = entry.get('rain', {}).get('3h', 0)

        # Track high and low temperatures
        if temp > daily_data[date]["high"]:
            daily_data[date]["high"] = temp
        if temp < daily_data[date]["low"]:
            daily_data[date]["low"] = temp

        # Accumulate precipitation
        daily_data[date]["precipitation_sum"] += precipitation

    # Format the forecast summary
    forecast_summary = []
    for date, data in daily_data.items():
        high_temp = data["high"]
        low_temp = data["low"]
        total_precipitation = data["precipitation_sum"]
        forecast_summary.append(f"Date: {date}, High: {high_temp}°F, Low: {low_temp}°F, Total Precipitation: {total_precipitation:.2f} mm")

    return forecast_summary[:5]  # Limit to 5 days

# Function to generate AI recommendations using gpt-3.5-turbo model
def generate_recommendations(forecast_summary):
    forecast_text = "\n".join(forecast_summary)
    
    # Prompt engineering for water conservation and usage tips
    prompt = (f"Based on the following 5-day weather forecast:\n{forecast_text}\n"
              "provide detailed water conservation and usage tips for a residential household. "
              "Consider weather conditions, temperatures, precipitation levels, and potential needs for water usage.")

    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that provides water conservation and usage tips based on weather data."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Streamlit app interface
def main():
    st.title("Weather-Based Water Conservation and Usage Assistant")

    # User input for city
    city = st.text_input("Enter a city for the forecast:", "San Francisco")

    # Fetch and display forecast and recommendations on button click
    if st.button("Get Forecast and Recommendations"):
        weather_data = get_weather_forecast(city)
        
        if weather_data:
            # Process forecast data to calculate daily highs, lows, and precipitation
            forecast_summary = process_forecast_data(weather_data)
            
            # Display daily high and low temperatures and total precipitation
            st.subheader(f"5-Day Weather Forecast for {city}")
            for forecast in forecast_summary:
                st.write(forecast)
            
            # Display AI-generated recommendations
            st.subheader("Household Water Conservation and Usage Tips")
            recommendations = generate_recommendations(forecast_summary)
            st.write(recommendations)

if __name__ == "__main__":
    main()




