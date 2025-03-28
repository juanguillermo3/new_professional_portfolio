import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import urllib.parse

# Load environment variables
load_dotenv(override=True)

# Environment configurations
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+573053658650" )

# Load freely available icons
HOME_ICON = "https://img.icons8.com/?size=100&id=hmZnke9jb8oq&format=png&color=000000"
RECSYS_ICON = "https://img.icons8.com/?size=100&id=NaOfOQ3MMYaq&format=png&color=000000"  # Updated icon for emphasis
SERVICES_ICON = "https://cdn-icons-png.flaticon.com/128/3135/3135706.png"

def render_multi_page_navigation():
    # Define Custom CSS for Navigation Bar and WhatsApp Button
    st.markdown(
        """
        <style>
            .fixed-navbar {
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 255, 255, 0.1);  /* Transparent background */
                backdrop-filter: blur(4px);  /* Frosted glass effect */
                border: 2px solid rgba(255, 255, 255, 0.9);
                box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.1);
                padding: 12px 24px;
                border-radius: 15px;
                display: flex;
                gap: 20px;
                align-items: center;
            }

            .nav-link {
                display: inline-block;
                text-decoration: none;
                transition: transform 0.2s ease-in-out;
            }

            .nav-link img {
                width: 50px;
                height: 50px;
                border-radius: 50%;
            }

            .nav-link:hover {
                transform: scale(1.1);
            }

            /* WhatsApp Button (Custom Style inside Navbar) */
            .nav-link.whatsapp-btn {
                background-color: #25D366;
                width: 55px;
                height: 55px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                transition: all 0.3s ease-in-out;
                position: relative;
            }

            .nav-link.whatsapp-btn img {
                width: 36px;
                height: 36px;
            }

            .nav-link.whatsapp-btn:hover {
                background-color: #1EBEA5;
                transform: scale(1.1);
            }

            /* Tooltip for WhatsApp */
            .nav-link.whatsapp-btn::after {
                content: "Let's chat on WhatsApp!";
                position: absolute;
                bottom: 70px;
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
            }

            .nav-link.whatsapp-btn:hover::after {
                opacity: 1;
                visibility: visible;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Hardcoded WhatsApp Number & Message
    whatsapp_number = WHATSAPP_NUMBER
    salutation = "Hello! I’d love to learn more about your services."
    whatsapp_url = f"https://wa.me/{whatsapp_number.replace('+', '')}?text={urllib.parse.quote(salutation)}"

    # **Navigation Links with WhatsApp Button**
    st.markdown(
        f"""
        <div class="fixed-navbar">
            <a href="?section=Home" class="nav-link">
                <img src="https://via.placeholder.com/50" alt="Home">
            </a>
            <a href="?section=RecSys" class="nav-link">
                <img src="https://via.placeholder.com/50" alt="Recommender System">
            </a>
            <a href="?section=Services" class="nav-link">
                <img src="https://via.placeholder.com/50" alt="Services and Rates">
            </a>
            <a href="{whatsapp_url}" target="_blank" class="nav-link whatsapp-btn">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/WhatsApp_icon.png">
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


