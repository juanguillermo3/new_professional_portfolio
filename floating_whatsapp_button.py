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
        <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/WhatsApp_icon.png">
        </a>
    """, unsafe_allow_html=True)
