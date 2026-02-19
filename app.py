import streamlit as st
import pandas as pd

# Import your agent
from backend.groq_agent import ask_agent

st.set_page_config(page_title="Drone Coordinator Agent")

st.title("🚁 Drone Operations Coordinator AI Agent")

st.write(
    "Ask about pilot assignments, drones, conflicts, or reassignments."
)

# Input box
query = st.text_input("Enter your request:")

# Button
if st.button("Submit"):

    if query.strip() == "":
        st.warning("Please enter a query.")

    else:
        response = ask_agent(query)

        st.subheader("Agent Response:")

        # If response is DataFrame → show table
        if isinstance(response, pd.DataFrame):
            st.dataframe(response)

        else:
            st.write(response)
