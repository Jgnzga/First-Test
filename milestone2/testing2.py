import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import openai
import os

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this is securely set

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Shower (L)", "Dishwashing (L)", "Laundry (L)", "Gardening (L)", "Drinking Water (L)"])

# Sidebar Inputs for Daily Water Usage
st.sidebar.title("Enter Daily Water Usage")
date = st.sidebar.date_input("Select Date", datetime.now())
household_size = st.sidebar.number_input("Number of people in household", min_value=1)

# Daily water activities with default values
shower_minutes = st.sidebar.number_input("Minutes spent in the shower", min_value=0)
dishwashing_loads = st.sidebar.number_input("Number of dishwashing loads", min_value=0)
laundry_loads = st.sidebar.number_input("Number of laundry loads", min_value=0)
gardening_minutes = st.sidebar.number_input("Minutes of outdoor water use", min_value=0)
drinking_water = st.sidebar.number_input("Drinking water in liters", min_value=0.0)

# Calculate estimated water usage (L) with average values
shower_usage = shower_minutes * 10  # Assume 10 L/min
dishwashing_usage = dishwashing_loads * 12  # Assume 12 L per dishwasher load
laundry_usage = laundry_loads * 50  # Assume 50 L per laundry load
gardening_usage = gardening_minutes * 15  # Assume 15 L/min for outdoor use
total_daily_usage = shower_usage + dishwashing_usage + laundry_usage + gardening_usage + drinking_water

# Submit button to log data
if st.sidebar.button("Log Today's Water Usage"):
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame({
        "Date": [date],
        "Shower (L)": [shower_usage],
        "Dishwashing (L)": [dishwashing_usage],
        "Laundry (L)": [laundry_usage],
        "Gardening (L)": [gardening_usage],
        "Drinking Water (L)": [drinking_water]
    })])
    st.success("Today's data logged successfully!")

# Display Data
st.title("Personalized Water Usage Tracker")
st.write("Track your water usage trends over time:")

# Calculate and display summary statistics
if not st.session_state.data.empty:
    df = st.session_state.data
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    weekly_avg = df.set_index("Date").resample("W").sum().mean()

    st.subheader("Weekly Average Water Usage (Liters)")
    st.write(weekly_avg)

    # Plotting daily water usage trends
    fig, ax = plt.subplots()
    df.set_index("Date").plot(kind="line", ax=ax)
    ax.set_ylabel("Water Usage (Liters)")
    ax.set_title("Daily Water Usage Trends")
    st.pyplot(fig)

    # Display recent data entries
    st.subheader("Recent Entries")
    st.write(df.tail())
else:
    st.write("No data logged yet. Please enter your daily water usage in the sidebar.")

# Define average water usage benchmarks per person per day
benchmark = {
    "Shower": 70,           # liters per person per day
    "Dishwashing": 12,      # liters per load (assume 1 load per person per day)
    "Laundry": 50,          # liters per load (assume 1 load per household per day)
    "Gardening": 30,        # liters per person per day
    "Drinking Water": 3     # liters per person per day
}

# Calculate water efficiency score
def calculate_efficiency_score(total_usage, household_size):
    # Calculate expected usage based on household size and benchmarks
    expected_usage = (benchmark["Shower"] + benchmark["Gardening"] + benchmark["Drinking Water"]) * household_size \
                     + benchmark["Dishwashing"] * household_size + benchmark["Laundry"]
    
    # Calculate efficiency score as a percentage
    score = max(0, min(100, (expected_usage / total_usage) * 100)) if total_usage > 0 else 100
    return score

# Display water efficiency score
if total_daily_usage > 0:
    st.subheader("Water Efficiency Score")
    efficiency_score = calculate_efficiency_score(total_daily_usage, household_size)
    st.write(f"Your Water Efficiency Score: {efficiency_score:.1f}/100")
    st.write("A higher score indicates more efficient water use relative to household size and activity levels.")

# Function to get water-saving tips from OpenAI API
def get_water_saving_tips(total_usage):
    prompt = f"You are an expert in water conservation. Based on a daily water usage of {total_usage} liters, suggest three specific actions to help reduce water usage at home."
    try:
        response = openai.ChatCompletion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.5
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating tips: {e}"

# Display personalized water-saving tips
if total_daily_usage > 0:
    st.subheader("Personalized Water-Saving Tips")
    tips = get_water_saving_tips(total_daily_usage)
    st.write(tips)
