import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import urllib.parse

# Load environment variables
load_dotenv(override=True)

# Environment configurations
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+573053658650")
WHATSAPP_ICON = os.getenv("WHATSAPP_ICON", "https://upload.wikimedia.org/wikipedia/commons/5/5e/WhatsApp_icon.png")

# Load freely available icons with default values
HOME_ICON = os.getenv("HOME_ICON", "https://img.icons8.com/?size=100&id=hmZnke9jb8oq&format=png&color=000000")
RECSYS_ICON = os.getenv("RECSYS_ICON", "https://img.icons8.com/?size=100&id=NaOfOQ3MMYaq&format=png&color=000000")
SERVICES_ICON = os.getenv("SERVICES_ICON", "https://cdn-icons-png.flaticon.com/128/3135/3135706.png")

def render_multi_page_navigation():
    # Define Custom CSS for a Frosted Glass Effect Navbar with Anchor Links
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
                padding: 10px 20px;
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
            /* WhatsApp Button */
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
                <img src="{HOME_ICON}" alt="Home">
            </a>
            <a href="?section=RecSys" class="nav-link">
                <img src="{RECSYS_ICON}" alt="Recommender System">
            </a>
            <a href="?section=Services" class="nav-link">
                <img src="{SERVICES_ICON}" alt="Services and Rates">
            </a>
            <a href="{whatsapp_url}" target="_blank" class="nav-link whatsapp-btn">
                <img src="{WHATSAPP_ICON}">
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )



