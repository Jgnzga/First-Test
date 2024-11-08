import streamlit as st

# Define each feature as a separate function
def chatbot_feature():
    st.header("Water Conservation Chatbot")
    # Add code for chatbot functionality here

def water_cost_calculator():
    st.header("Water Cost Calculator")
    # Add code for cost calculation here

def third_feature():
    st.header("Additional Water Saving Feature")
    # Add code for third feature here

# Main page with navigation
st.title("Water Conservation App")

# Create a sidebar or radio button for navigation
feature_choice = st.sidebar.radio("Choose a Feature:", 
                                  ("Chatbot", "Cost Calculator", "Third Feature"))

# Display the selected feature
if feature_choice == "Chatbot":
    chatbot_feature()
elif feature_choice == "Cost Calculator":
    water_cost_calculator()
elif feature_choice == "Third Feature":
    third_feature()
