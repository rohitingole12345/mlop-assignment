import streamlit as st
from textblob import TextBlob

# Title of the app
st.title("Basic Sentiment Analysis")
st.write("Enter text to determine its sentiment (positive, negative, or neutral).")

# User input
user_input = st.text_area("Enter your text:")

if st.button("Analyze Sentiment"):
    if user_input.strip():
        # Perform sentiment analysis
        blob = TextBlob(user_input)
        sentiment = blob.sentiment.polarity

        # Determine sentiment
        if sentiment > 0:
            st.success("The sentiment is **Positive**.")
        elif sentiment < 0:
            st.error("The sentiment is **Negative**.")
        else:
            st.info("The sentiment is **Neutral**.")
    else:
        st.warning("Please enter some text to analyze.")
