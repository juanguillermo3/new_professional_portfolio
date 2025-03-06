import os
import urllib.parse
import streamlit as st

def display_floating_buttons_container():
    """Creates a fixed container at the bottom of the screen to hold floating buttons."""
    st.markdown("""
        <style>
        .floating-button-container {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 15px;
            align-items: center;
            z-index: 9999;
        }
        </style>
        <div class="floating-button-container">
        """, unsafe_allow_html=True)

def close_floating_buttons_container():
    """Closes the floating button container div."""
    st.markdown("</div>", unsafe_allow_html=True)
