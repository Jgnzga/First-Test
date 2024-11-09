import streamlit as st
import pages.weather as weather
import pages.WaterMeterCalculatorAPI as water_meter
import pages.watercalc2 as water_calculator

# Main page with navigation
st.title("Water Conservation App")

# Sidebar navigation for different features
feature_choice = st.sidebar.radio("Choose a Feature:", 
                                  ("Weather Analysis", "Water Meter Tracker", "Water Usage Calculator"))

# Display the selected feature
if feature_choice == "Weather Analysis":
    weather.main()  # Calls the main function in weather.py
elif feature_choice == "Water Meter Tracker":
    water_meter.main()  # Calls the main function in WaterMeterCalculatorAPI.py
elif feature_choice == "Water Usage Calculator":
    water_calculator.main()  # Calls the main function in watercalc2.py
