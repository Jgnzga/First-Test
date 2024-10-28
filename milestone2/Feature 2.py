import streamlit as st

# Constants for water rates (cost per 100 cubic feet)
RATE_SINGLE_FAMILY_FIRST_TIER = 3.45  # for first 172 gpd
RATE_SINGLE_FAMILY_SECOND_TIER = 4.74  # for 172-393 gpd
RATE_SINGLE_FAMILY_THIRD_TIER = 6.27  # for over 393 gpd
GALLONS_PER_CCF = 748  # 1 CCF = 748 gallons

# Function to calculate the price of water
def calculate_price(gallons, time_of_day):
    ccf = gallons / GALLONS_PER_CCF  # Convert gallons to CCF

    # Determine rate based on time of day
    if time_of_day >= 0 and time_of_day < 6:  # Off-peak hours
        rate = RATE_SINGLE_FAMILY_FIRST_TIER
    elif time_of_day >= 6 and time_of_day < 18:  # Peak hours
        rate = RATE_SINGLE_FAMILY_SECOND_TIER
    else:  # Evening hours
        rate = RATE_SINGLE_FAMILY_THIRD_TIER

    # Calculate total cost
    total_cost = ccf * rate
    return total_cost

# Streamlit UI
st.set_page_config(page_title="Water Cost Calculator", layout="centered")
st.title("💧 Water Cost Calculator")
st.write("Calculate the cost of water usage based on gallons and time of day.")

# User inputs for gallons and time of day
gallons = st.number_input("Enter the number of gallons:", min_value=1, value=300)
time_of_day = st.number_input("Enter the time of day (0-23):", min_value=0, max_value=23, value=8)

# Calculate and display the price
if st.button("Calculate Price"):
    price = calculate_price(gallons, time_of_day)
    st.success(f"The price for {gallons} gallons of water at {time_of_day}:00 is: ${price:.2f}")
