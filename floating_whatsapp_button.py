"""
title: Floating Whatsapp Button
description: Renders a floating component for whatsapp communication. Servers as a contant invitiation to the client to stablish a connection.
"""

import os
import urllib.parse
import streamlit as st

def display_floating_whatsapp_button(
    whatsapp_number: str = None,
    button_radius: int = 75,
    horizontal_position: str = "65%",
    salutation: str = "I want to know more about your services",
    hover_text: str = "Juan says: Let's connect"
):
    """
    Displays a floating WhatsApp button in Streamlit with a hover message and an optional pre-filled salutation.

    Parameters:
        whatsapp_number (str, optional): The WhatsApp number in international format (e.g., +1234567890).
                                          If not provided, it will be read from the environment.
        button_radius (int, optional): The diameter of the circular button in pixels (default: 110px).
        horizontal_position (str, optional): The horizontal position in CSS units (default: "65%").
        salutation (str, optional): A pre-filled message for the chat (default: "I want to know more about your services").
        hover_text (str, optional): The text that appears when hovering over the button (default: "Juan says: Let's connect").

    Mapping to WhatsApp Request:
        - whatsapp_number → `https://wa.me/<whatsapp_number>`
        - salutation → `text=<URL_ENCODED_MESSAGE>` (pre-fills the WhatsApp chat)
        - The button appears as a floating element, fixed at the bottom of the page.
    """

    # Read from environment if not provided
    if whatsapp_number is None:
        whatsapp_number = os.getenv("WHATSAPP_NUMBER", "").strip()

    # Ensure valid number
    if not whatsapp_number:
        st.warning("WhatsApp button is not displayed because no number was provided.")
        return

    # URL Encode the message
    encoded_message = urllib.parse.quote(salutation)

    # Create WhatsApp link with pre-filled message
    whatsapp_url = f"https://wa.me/{whatsapp_number.replace('+', '')}?text={encoded_message}"

    st.markdown(f"""
        <style>
        .whatsapp-btn {{
            position: fixed;
            bottom: 20px;
            left: {horizontal_position};
            transform: translateX(-50%);
            background-color: #25D366;
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

        .whatsapp-btn img {{
            width: {button_radius * 0.64}px;
            height: {button_radius * 0.64}px;
        }}

        .whatsapp-btn:hover {{
            background-color: #1EBEA5;
            cursor: pointer;
        }}

        /* Tooltip Styling */
        .whatsapp-btn::after {{
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

        .whatsapp-btn:hover::after {{
            opacity: 1;
            visibility: visible;
        }}
        </style>

        <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/WhatsApp_icon.png">
        </a>
    """, unsafe_allow_html=True)
