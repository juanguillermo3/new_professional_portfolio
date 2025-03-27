"""
title: Web Application
description: Streamlit based Front-End application for my professional portfolio. 
"""

import streamlit as st
import os
from dotenv import load_dotenv
from git_api_utils import load_repos_metadata, load_modules_metadata, REPOS_IN_PORTFOLIO
from professional_bio import cv
from front_end_utils import render_section_separator
from hero_area import hero
from rec_sys import recsys
from about_section import about
from services_section import services
from socials_section import socials
from testimonials import testimonials
from floating_whatsapp_button import  display_floating_whatsapp_button
from floating_linkedin_button import display_floating_linkedin_button
from floating_buttons import display_floating_buttons_container, close_floating_buttons_container
from multi_page_navigation import render_multi_page_navigation

# Load environment variables
load_dotenv(override=True)

# Environment configurations
ENVIRONMENT = os.getenv("ENVIRONMENT")
REPO_OWNER = os.getenv("REPO_OWNER")
LINKEDIN_PROFILE = os.getenv("LINKEDIN_PROFILE")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+573053658650" )

# Define available sections for customization
SECTIONS = {
    "About": about,
    "RecSys": recsys,
    "Services&Rates": services,
    "Curriculum Vitae": cv,
    #"Socials": socials,
    "Testimonials": testimonials
}
# **Customization Options**
if "selected_sections" not in st.session_state:
    st.session_state["selected_sections"] = list(SECTIONS.keys())

st.markdown("""
    <style>
        body, .stApp {
            background-color: #ffffff !important;  /* Pure white background */
            color: #333333 !important;  /* Dark gray font for readability */
        }
        
        /* Ensuring text inside all Streamlit components remains consistent */
        .stTextInput, .stMarkdown, .stDataFrame, .stSelectbox, .stButton {
            color: #333333 !important;
        }
    </style>
    """, unsafe_allow_html=True)


# Example usage of the multiselect widget
selected_sections = st.multiselect(
    "Customize which sections to display. Refresh the page for a full view.",
    options=SECTIONS.keys(),
    default=st.session_state["selected_sections"]
)



# **Title Section**
st.markdown("""
    <style>
    h1 {
        font-size: 4em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)



st.title("Welcome to My Professional Site")

# **Hero Section (Always Rendered)**
hero.render()
render_section_separator()
render_section_separator()

# **Render Sections Conditionally**
for section_name, module in SECTIONS.items():
    if section_name in selected_sections:
        module.render()
        render_section_separator()



#display_floating_whatsapp_button( whatsapp_number=WHATSAPP_NUMBER, horizontal_position= "65%",)

# Load freely available icons
HOME_ICON = "https://img.icons8.com/?size=100&id=hmZnke9jb8oq&format=png&color=000000"
RECSYS_ICON = "https://img.icons8.com/?size=100&id=NaOfOQ3MMYaq&format=png&color=000000"  # Updated icon for emphasis
SERVICES_ICON = "https://cdn-icons-png.flaticon.com/128/3135/3135706.png"
# HTML layout for navbar
st.markdown(
    f"""
    <div class="fixed-navbar">
        <button class="nav-button" onclick="window.location.href='/Home'">
            <img src="{HOME_ICON}" alt="Home">
        </button>
        <button class="nav-button" onclick="window.location.href='/RecSys'">
            <img src="{RECSYS_ICON}" alt="Recommender System">
        </button>
        <button class="nav-button" onclick="window.location.href='/Services'">
            <img src="{SERVICES_ICON}" alt="Services and Rates">
        </button>
    </div>
    """,
    unsafe_allow_html=True,
)
# Custom CSS for fixed-position frosted glass navbar
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
        .nav-button {
            background: none;
            border: none;
            cursor: pointer;
        }
        .nav-button img {
            width: 50px;
            height: 50px;
            transition: transform 0.2s ease-in-out;
        }
        .nav-button img:hover {
            transform: scale(1.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)




