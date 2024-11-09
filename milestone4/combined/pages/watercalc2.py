import os
import streamlit as st
import openai  # Import OpenAI library for generating advice

# Access the API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")  # Ensure the API key is set in your environment as "OPENAI_API_KEY"
if openai_api_key is None:
    st.error("OpenAI API key is not set. Please set the environment variable OPENAI_API_KEY.")
else:
    openai.api_key = openai_api_key

def generate_water_saving_advice(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")  # Ensure the API key is set in your environment as "OPENAI_API_KEY"
    if openai_api_key is None:
        st.error("OpenAI API key is not set. Please set the environment variable OPENAI_API_KEY.")
    else:
        openai.api_key = openai_api_key
    # Centered Logo and Title with EBMUD Link
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='file:///Users/sams/Desktop/New Water/water2.png' width='150'>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("# Water Conservation Utility Guide")
    st.markdown("**Based on data from [EBMUD](https://www.ebmud.com/water/water-rates/rates-and-fees-schedules)**")
    st.write("Input your household information below to estimate your water usage and see potential savings by adopting water conservation habits.")

    # Input Data
    st.subheader("Household Information")
    household_size = st.number_input("Number of People in the House", min_value=1, value=3)
    lawn_size = st.number_input("Size of Lawn (sq ft)", min_value=0, value=500)
    lawn_watering_frequency = st.slider("How many times do you water your lawn per week?", 0, 7, 3)
    has_pool = st.selectbox("Do you have a pool?", ("Yes", "No"))

    # Pool-related inputs
    if has_pool == "Yes":
        pool_volume = st.number_input("Volume of the pool (gallons)", min_value=500, value=10000)
        pool_renew_frequency = st.slider("How often do you clean/renew pool water? (times per month)", 0, 4, 1)
    else:
        pool_volume = 0
        pool_renew_frequency = 0

    # Constants for calculation
    avg_daily_usage_per_person = 100  # gallons per day per person
    lawn_watering_rate = 0.62  # gallons per sq ft per watering
    pool_evaporation_rate = 0.003  # approx 0.3% of pool volume lost daily

    # Calculate water usage
    people_usage = household_size * avg_daily_usage_per_person
    lawn_usage = lawn_size * lawn_watering_rate * lawn_watering_frequency
    pool_usage = pool_volume * pool_evaporation_rate * 30 + (pool_renew_frequency * pool_volume)
    total_monthly_usage = people_usage * 30 + lawn_usage * 4 + pool_usage  # monthly estimate

    # Estimation of Bill Impact
    rate_per_gallon = 0.005  # example rate in dollars per gallon
    estimated_monthly_bill = total_monthly_usage * rate_per_gallon

    # Display usage and bill estimates
    st.subheader("Estimated Water Usage")
    st.write(f"Estimated Monthly Water Usage: {total_monthly_usage:.2f} gallons")
    st.write(f"Estimated Monthly Water Bill: ${estimated_monthly_bill:.2f}")

    # Tips & Tricks Button with API-Generated Advice
    if st.button("Possible Solutions"):
        st.subheader("Tips for Reducing Water and Waste")
        
        # Generate dynamic advice based on OpenAI's API
        prompt = (
            "Provide tips and practical advice on reducing household water usage. "
            "Consider factors such as lawn watering, pool maintenance, shower length, and general water-saving behaviors."
        )
        
        advice = generate_water_saving_advice(prompt)
        st.write(advice)

    # Customize interactivity for users
    st.write("For more personalized solutions, try adjusting the values in the calculator.")
if __name__ == "__main__":
    main()