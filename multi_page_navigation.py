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
CV_ICON = os.getenv("SERVICES_ICON", "https://img.icons8.com/?size=100&id=kZDsMIbqetN3&format=png&color=000000")


import streamlit as st
import urllib.parse

def render_multi_page_navigation():
    st.markdown(
        """
        <style>
            .fixed-navbar {
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(4px);
                border: 2px solid rgba(255, 255, 255, 0.9);
                box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.1);
                padding: 10px 20px;
                border-radius: 15px;
                display: flex;
                gap: 20px;
                align-items: center;
                z-index: 9999;
                max-width: 95vw;
                flex-wrap: wrap;
            }

            .nav-link {
                display: inline-flex;
                text-decoration: none;
                transition: transform 0.2s ease-in-out;
                position: relative;
            }

            .nav-link img {
                width: 50px;
                height: auto;
                max-height: 50px;
                aspect-ratio: 1 / 1;
                border-radius: 50%;
            }

            .nav-link:hover {
                transform: scale(1.1);
            }

            .nav-link::after {
                content: attr(data-tooltip);
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

            .nav-link:hover::after {
                opacity: 1;
                visibility: visible;
            }

            .nav-link.whatsapp-btn {
                background-color: #25D366;
                width: 66px;  /* 120% of 55px */
                height: 66px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                transition: all 0.3s ease-in-out;
                position: relative;
                margin-left: auto;
            }

            .nav-link.whatsapp-btn img {
                width: 42px;
                height: 42px;
            }

            .nav-link.whatsapp-btn:hover {
                background-color: #1EBEA5;
                transform: scale(1.1);
            }

            @media (max-width: 500px) {
                .nav-link img {
                    width: 40px;
                    max-height: 40px;
                }

                .nav-link.whatsapp-btn {
                    width: 58px;
                    height: 58px;
                }

                .nav-link.whatsapp-btn img {
                    width: 36px;
                    height: 36px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    whatsapp_number = WHATSAPP_NUMBER
    salutation = "Hello! I’d love to learn more about your services."
    whatsapp_url = f"https://wa.me/{whatsapp_number.replace('+', '')}?text={urllib.parse.quote(salutation)}"

    st.markdown(
        f"""
        <div class="fixed-navbar">
            <a href="?section=Home" class="nav-link" data-tooltip="Go to Home">
                <img src="{HOME_ICON}" alt="Home">
            </a>
            <a href="?section=RecSys" class="nav-link" data-tooltip="Explore Recommendations">
                <img src="{RECSYS_ICON}" alt="Recommender System">
            </a>
            <a href="?section=Services" class="nav-link" data-tooltip="View Services and Rates">
                <img src="{SERVICES_ICON}" alt="Services and Rates">
            </a>
            <a href="?section=CurriculumVitae" class="nav-link" data-tooltip="View Curriculum Vitae">
                <img src="{CV_ICON}" alt="Curriculum Vitae">
            </a>
            <a href="{whatsapp_url}" target="_blank" class="nav-link whatsapp-btn" data-tooltip="Chat on WhatsApp">
                <img src="{WHATSAPP_ICON}">
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )




