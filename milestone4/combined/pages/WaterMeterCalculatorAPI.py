import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Load interval data from CSV file
def load_interval_data(file_path):
    # Load CSV data into a DataFrame
    df = pd.read_csv(file_path)
    return df

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
def main():
        
    # Streamlit app
    st.title("Water Usage Tracker")

    # Load data from CSV file
    file_path = 'synthetic_water_usage_data.csv'  # Ensure this file is in the same directory or provide the full path
    interval_data = load_interval_data(file_path)

    # Set date range for display
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    st.subheader(f"Water Usage Data (from {start_date} to {end_date})")

    # Calculate total usage over the past 7 days
    recent_data = interval_data[(interval_data['start'] >= start_date) & (interval_data['start'] <= end_date)]
    if not recent_data.empty:
        total_usage = recent_data['kwh'].sum()
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
    \text{Average Expected Usage} = \text{Number of People} \times 50 \, \text{gallons/person/day} \times 7 \, \text{days}
    \]

    - Your score is calculated as follows:

    \[
    \text{Efficiency Score} = 100 - \left(\frac{\text{Total Usage}}{\text{Average Expected Usage}} \times 100\right)
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

if __name__ == "__main__":
    main()
