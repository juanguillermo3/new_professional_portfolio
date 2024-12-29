import streamlit as st

# Minimal Streamlit App
st.title("Welcome to My Streamlit App!")
st.write("This is a simple, interactive app powered by Streamlit.")

# Example widget
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}! 👋")
