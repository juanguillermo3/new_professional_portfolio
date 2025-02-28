"""
title: Floating Whatsapp Button
description: Renders a floating component for whatsapp communication. Servers as a contant invitiation to the client to stablish a connection.
"""

import streamlit as st
import os

def display_floating_whatsapp_button(
    whatsapp_number: str = None,
    salutation: str = "I want to know more about your services.",
    hover_text: str = "Juan says: Let's connect",
    button_radius: int = 60,
    horizontal_position: float = 0.65
):
    """
    Displays a floating WhatsApp button with customizable options.
    
    Parameters:
    - whatsapp_number (str, optional): The WhatsApp number to contact. Defaults to reading from env.
    - salutation (str, optional): The pre-filled message sent when clicking. Default: "I want to know more about your services."
    - hover_text (str, optional): The pop-up text shown on hover. Default: "Juan says: Let's connect."
    - button_radius (int, optional): The size of the button (default: 60px).
    - horizontal_position (float, optional): The horizontal placement as a fraction of screen width (default: 0.65).
    
    This function generates a floating WhatsApp button at the bottom-right corner of the page.
    """
    
    # Read from environment if not provided
    if whatsapp_number is None:
        whatsapp_number = os.getenv("WHATSAPP_NUMBER", "1234567890")  # Default fallback
    
    # Construct the WhatsApp link
    whatsapp_link = f"https://wa.me/{whatsapp_number}?text={salutation.replace(' ', '%20')}"
    
    # Custom HTML for floating button
    button_html = f"""
    <style>
        .floating-whatsapp {{
            position: fixed;
            bottom: 20px;
            left: {horizontal_position * 100}%;
            transform: translateX(-50%);
            width: {button_radius}px;
            height: {button_radius}px;
            background-color: #25D366;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease-in-out;
            cursor: pointer;
        }}
        .floating-whatsapp:hover::after {{
            content: "{hover_text}";
            position: absolute;
            bottom: 110%;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            white-space: nowrap;
            font-size: 14px;
        }}
    </style>
    <a href="{whatsapp_link}" target="_blank" class="floating-whatsapp">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="{button_radius * 0.6}px">
    </a>
    """
    
    # Render in Streamlit
    st.markdown(button_html, unsafe_allow_html=True)
