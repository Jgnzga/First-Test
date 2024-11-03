import streamlit as st
import os
import requests
from datetime import datetime, timedelta
import openai


# Function to get meter data (replace with your actual API call)
def get_meter_data():
    return {
        "uid": "example-meter-uid",
        "name": "Home Water Meter"
    }

# Function to get interval data (replace with your actual API call)
def get_interval_data(meter_uid, start_date, end_date):
    return {
        "intervals": [
            {"start": "2024-10-27T12:00:00Z", "kwh": 50},
            {"start": "2024-10-28T12:00:00Z", "kwh": 30},
            {"start": "2024-10-29T12:00:00Z", "kwh": 70},
            {"start": "2024-10-30T12:00:00Z", "kwh": 40},
            {"start": "2024-10-31T12:00:00Z", "kwh": 60},
            {"start": "2024-11-01T12:00:00Z", "kwh": 90},
            {"start": "2024-11-02T12:00:00Z", "kwh": 80}
        ]
    }

# Function to calculate total usage
def calculate_usage(reading, unit):
    return reading  # Assuming input is already in gallons for simplicity

# Function to calculate efficiency score
def calculate_efficiency_score(total_usage, num_people):
    average_daily_usage = 50 * num_people  # 50 gallons per person per day
    average_usage = average_daily_usage * 7  # For 7 days
    efficiency_score = (total_usage / average_usage) * 100
    return 100 - efficiency_score, average_usage  # Invert the score

# Suggestions based on efficiency score
def get_suggestions(efficiency_score):
    if efficiency_score < 0:  # Inefficient usage
        return [
            "Your water usage is higher than expected. Consider reducing shower times and fixing leaks.",
            "Try using a broom instead of a hose to clean driveways and sidewalks.",
            "You might want to check your irrigation system for leaks or inefficiencies.",
            "Consider installing water-saving fixtures to enhance your conservation efforts."
        ]
    else:  # Efficient usage
        return [
            "Excellent job! You're using water very efficiently.",
            "Consider maintaining your current habits to keep conserving water.",
            "Look into rainwater harvesting systems to enhance your efficiency."
        ]

# Function to get chatbot response (define your logic here)
def get_chatbot_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message['content']
# Streamlit app
st.title("Water Usage Tracker")

# Get meter data
meter = get_meter_data()

# Set date range for interval data
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')
st.subheader(f"Water Usage Data (from {start_date} to {end_date})")

# Fetch and display interval data for this meter
interval_data = get_interval_data(meter['uid'], start_date, end_date)
if interval_data:
    total_usage = sum(interval['kwh'] for interval in interval_data['intervals'])  # Replace "kwh" if necessary
    st.write(f"Total Usage in Last 7 Days: {total_usage:.2f} gallons")

    # Set number of people input
    number_of_people = st.number_input("Number of people in household:", min_value=1, value=1)

    # Calculate efficiency score
    efficiency_score, avg_usage = calculate_efficiency_score(total_usage, number_of_people)
    st.write(f"Efficiency Score: {efficiency_score:.2f}% (compared to an average of {avg_usage:.2f} gallons)")

    # Provide explanation of the efficiency score
    st.markdown("""
### Understanding Your Efficiency Score

- **Efficiency Score**: This score measures your water usage against an average expected usage based on the number of people in your household.

- The average expected usage is calculated using the formula:

  \[
  \t{Average Expected Usage} = \t{Number of People} \tX 50 \, \t{gallons/person/day} \tX 7 \, \t{days}
  \]

- Your score is calculated as follows:

  \[
  \t{Efficiency Score} = 100 - \t{Total Usage}/{\t{Average Expected Usage} \tX 100)
  \]

- A score of **0%** means your usage is exactly at the expected amount.
- A score **above 0%** indicates more efficient water usage.
- A score below **0%** suggests you may have room for improvement in your water conservation practices.
""")

    # Provide suggestions based on efficiency score
    suggestions = get_suggestions(efficiency_score)
    st.write("### Suggestions:")
    for suggestion in suggestions:
        st.write(f"- {suggestion}")

    # Display usage intervals
    st.subheader("Detailed Usage Intervals:")
    from datetime import datetime

    # Display usage intervals with formatted date and time
    for interval in interval_data['intervals']:
        start_time = datetime.fromisoformat(interval['start'])
        formatted_start = start_time.strftime('%Y-%m-%d %H:%M:%S')
        st.write(f"Start: {formatted_start}, Usage: {interval['kwh']} gallons")
else:
    st.write("No interval data available for this meter.")

# Chatbot section
st.markdown("### Ask the Water Habits Chatbot:")
user_input = st.text_input("What would you like to know about water habits?")
    
if st.button("Ask"):
    if user_input:
        response = get_chatbot_response(user_input)
        st.write("**Chatbot Response:**")
        st.write(response)
    else:
        st.write("Please enter a question to ask the chatbot.")
