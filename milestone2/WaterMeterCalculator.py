import streamlit as st
import os
import openai

# Set the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
HCF_TO_GALLONS = 748.05  # 1 HCF = 748.05 gallons
CCF_TO_GALLONS = 1000  # 1 CCF = 1000 gallons
AVG_WATER_USAGE_PER_PERSON = 80  # Average gallons used per person per day
DAYS_IN_MONTH = 30  # Average days in a month

# Function to calculate total water usage
def calculate_usage(reading, unit):
    if unit == 'HCF':
        total_gallons = reading * HCF_TO_GALLONS
    else:
        total_gallons = reading * CCF_TO_GALLONS
    return total_gallons

# Function to calculate efficiency score
def calculate_efficiency_score(total_usage, num_people):
    avg_usage = AVG_WATER_USAGE_PER_PERSON * num_people * DAYS_IN_MONTH
    efficiency_score = (avg_usage - total_usage) / avg_usage * 100
    return efficiency_score, avg_usage

# Function to get suggestions based on efficiency score
def get_suggestions(efficiency_score):
    if efficiency_score < 0:
        return [
            "Install a low-flow showerhead to save gallons per shower.",
            "Consider collecting rainwater for outdoor use.",
            "Turn off the tap while brushing teeth or shaving.",
            "Use mulch in your garden to retain moisture.",
            "Check for and repair leaks in irrigation systems."
        ]
    else:
        return [
            "Use a timer while watering your garden to avoid overwatering.",
            "Install a smart irrigation system that adapts to weather conditions.",
            "Consider xeriscaping to reduce water usage.",
            "Regularly check your water bill for unusual spikes.",
            "Educate your household members about water-saving habits."
        ]

# Function to generate a response from the chatbot
# Function to generate a response from the chatbot
def get_chatbot_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message['content']
    

# Main app
def main():
    st.title("Household Water Usage Efficiency Tool \n*Requires You To Find Home Water Meter Information*")
    
    # User input
    reading = st.number_input("Enter your water meter reading:", min_value=0.0)
    unit = st.selectbox("Select the unit of measurement:", ("HCF", "CCF"))
    num_people = st.number_input("Enter the number of people in your household:", min_value=1)

    if st.button("Calculate Efficiency"):
        # Calculate total usage
        total_usage = calculate_usage(reading, unit)

        # Calculate efficiency score and average usage
        efficiency_score, avg_usage = calculate_efficiency_score(total_usage, num_people)

        # Display results
        st.write(f"Total water usage for the month: {total_usage:.2f} gallons")
        st.write(f"Efficiency score: {efficiency_score:.2f}% (compared to an average of {avg_usage:.2f} gallons)")

        # Provide explanation of the efficiency score
        st.markdown("""
        ### Understanding Your Efficiency Score
        - **Efficiency Score**: This score represents how your water usage compares to the average expected usage for your household size. 
        - A score of **100%** means you used exactly the average amount of water. 
        - A positive score indicates that you used less water than average, while a negative score means you used more than expected.
        """)

        # Provide suggestions based on efficiency score
        suggestions = get_suggestions(efficiency_score)
        st.write("### Suggestions:")
        for suggestion in suggestions:
            st.write(f"- {suggestion}")

    # Chatbot for water habits
    st.markdown("### Ask the Water Habits Chatbot:")
    user_input = st.text_input("What would you like to know about water habits?")
    
    if st.button("Ask"):
        if user_input:
            response = get_chatbot_response(user_input)
            st.write("**Chatbot Response:**")
            st.write(response)
        else:
            st.write("Please enter a question to ask the chatbot.")

if __name__ == "__main__":
    main()
