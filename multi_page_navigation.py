
import streamlit as st
from PIL import Image

# Load freely available icons
HOME_ICON = "https://img.icons8.com/?size=100&id=hmZnke9jb8oq&format=png&color=000000"
RECSYS_ICON = "https://img.icons8.com/?size=100&id=NaOfOQ3MMYaq&format=png&color=000000"  # Updated icon for emphasis
SERVICES_ICON = "https://cdn-icons-png.flaticon.com/128/3135/3135706.png"


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
                border-radius: 50%; /* Optional: Rounded icon look */
            }
            .nav-link:hover {
                transform: scale(1.1);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # **Navigation Links using `<a>` tags**
    st.markdown(
        f"""
        <div class="fixed-navbar">
            <a href="?section=Home" class="nav-link">
                <img src="{HOME_ICON}" alt="Home">
            </a>
            <a href="?section=RecSys" class="nav-link">
                <img src="{RECSYS_ICON}" alt="Recommender System">
            </a>
            <a href="?section=Services&Rates" class="nav-link">
                <img src="{SERVICES_ICON}" alt="Services and Rates">
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

