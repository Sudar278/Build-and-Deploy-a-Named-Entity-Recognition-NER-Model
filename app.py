import streamlit as st
import requests
import pandas as pd

# API Configuration
API_URL = "http://127.0.0.1:8000/predict"  # Update with your API endpoint
API_KEY = "f7a6dcb9832b47e8b81c4c5c13f0a2d6"  # Replace with your actual API key

# Streamlit UI
st.title("🔍 Named Entity Recognition (NER) App")
st.markdown("Enter text below to extract named entities.")

# Input Text Box
user_input = st.text_area("Enter your text here:", height=150)

# Button to trigger prediction
if st.button("Analyze Entities"):
    if user_input.strip():
        # Send request to API
        headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
        data = {"text": user_input}

        with st.spinner("Processing..."):
            try:
                response = requests.post(API_URL, json=data, headers=headers)
                result = response.json()

                if response.status_code == 200:
                    entities = result.get("entities", [])

                    if entities:
                        # Convert to DataFrame for display
                        df = pd.DataFrame(entities)
                        df.rename(columns={"word": "Entity", "entity_group": "Category", "score": "Confidence"}, inplace=True)
                        df["Confidence"] = df["Confidence"].apply(lambda x: round(x, 4))  # Round confidence scores
                        st.success("Entities Extracted Successfully!")
                        st.dataframe(df)  # Display as a table
                    else:
                        st.warning("No entities found in the text.")

                else:
                    st.error(f"API Error: {result.get('detail', 'Unknown error')}")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {str(e)}")

    else:
        st.warning("Please enter some text.")

