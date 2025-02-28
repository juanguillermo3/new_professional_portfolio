"""
title: Floating Linkedin Button
description: Renders a floating component for Linkedin account.
""

import os
import streamlit as st

def display_floating_linkedin_button(
    linkedin_url: str = None,
    button_radius: int = 75,
    horizontal_position: str = "55%",
    hover_text: str = "Juan says: Join my professional network."
):
    """
    Displays a floating LinkedIn button in Streamlit with a hover message.

    Parameters:
        linkedin_url (str, optional): The LinkedIn profile URL.
                                      If not provided, it will be read from the environment.
        button_radius (int, optional): The diameter of the circular button in pixels (default: 75px).
        horizontal_position (str, optional): The horizontal position in CSS units (default: "55%").
        hover_text (str, optional): The text that appears when hovering over the button.
        
    The button appears as a floating element, fixed at the bottom of the page.
    """

    # Read from environment if not provided
    if linkedin_url is None:
        linkedin_url = os.getenv("LINKEDIN_URL", "").strip()

    # Ensure valid URL
    if not linkedin_url:
        st.warning("LinkedIn button is not displayed because no profile URL was provided.")
        return

    st.markdown(f"""
        <style>
        .linkedin-btn {{
            position: fixed;
            bottom: 20px;
            left: {horizontal_position};
            transform: translateX(-50%);
            background-color: #0077B5;
            width: {button_radius}px;
            height: {button_radius}px;
            border-radius: 50%;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            transition: all 0.3s ease-in-out;
        }}

        .linkedin-btn img {{
            width: {button_radius * 0.64}px;
            height: {button_radius * 0.64}px;
        }}

        .linkedin-btn:hover {{
            background-color: #005582;
            cursor: pointer;
        }}

        /* Tooltip Styling */
        .linkedin-btn::after {{
            content: "{hover_text}";
            position: absolute;
            bottom: {button_radius + 10}px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #333;
            color: white;
            padding: 6px 12px;
            border-radius: 5px;
            font-size: 14px;
            white-space: nowrap;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease-in-out, visibility 0.3s;
        }}

        .linkedin-btn:hover::after {{
            opacity: 1;
            visibility: visible;
        }}
        </style>

        <a href="{linkedin_url}" target="_blank" class="linkedin-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png">
        </a>
    """, unsafe_allow_html=True)
