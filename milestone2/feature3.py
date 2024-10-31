import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="OPEN_API_KEY")

# Set up OpenAI API key

# Streamlit page setup
st.title("AI-Generated Water-Saving Advice")
st.write("Provide the details below to get personalized water-saving advice.")

# User Inputs
weather_condition = st.selectbox("Current Weather Condition", ["Sunny", "Rainy", "Cloudy", "Windy"])
recent_rain = st.radio("Did it rain recently?", ["Yes", "No"])
temperature = st.slider("Current Temperature (°C)", min_value=0, max_value=50, value=25)

# Generate advice
if st.button("Get Water-Saving Advice"):
    # New prompt structure for ChatCompletion
    messages = [
        {"role": "system", "content": "You are a helpful assistant providing water-saving advice."},
        {"role": "user", "content": f"The weather is {weather_condition}, it recently rained: {recent_rain}, and the temperature is {temperature}°C. Please provide water-saving advice."}
    ]

    # OpenAI API call with new ChatCompletion method
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # or "gpt-4" if available
    messages=messages,
    max_tokens=100)

    advice = response.choices[0].message.content
    st.write("### Water-Saving Advice")
    st.write(advice)
