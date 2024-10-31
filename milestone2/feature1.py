import openai
import streamlit as st

# Set up OpenAI API key
openai.api_key = 'OPEN_API_KEY'

# Function to generate a water-saving response from the AI
def get_water_saving_advice(user_question):
    prompt = f"Answer the following question with specific water-saving tips: '{user_question}'"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a water conservation expert providing water-saving advice."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]

# Streamlit App Interface
st.title("💬 Ask the AI Chatbot")
st.write("Ask a water-saving question (e.g., 'How can I save water while gardening?')")

# User input field for the question
user_question = st.text_input("Enter your question:")

# Button to get the response
if st.button("Ask"):
    if user_question:
        # Get the water-saving advice
        advice = get_water_saving_advice(user_question)

        # Display the advice
        st.subheader("Here's your water-saving advice:")
        st.write(advice)
    else:
        st.error("Please enter a question to get advice.")
