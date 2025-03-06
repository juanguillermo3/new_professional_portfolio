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

#display_floating_buttons_container()
display_floating_linkedin_button( linkedin_url=LINKEDIN_PROFILE, horizontal_position= "75%",)
display_floating_whatsapp_button( whatsapp_number=WHATSAPP_NUMBER, horizontal_position= "50%",)
#close_floating_buttons_container()

st.title("Welcome to My Professional Site")

# **Hero Section (Always Rendered)**
hero.render()
render_section_separator()

# **Customization Options**
if "selected_sections" not in st.session_state:
    st.session_state["selected_sections"] = list(SECTIONS.keys())

# Adding custom CSS for customizing the pills' appearance with a navy blue color
st.markdown("""
    <style>
        /* Customizing the pills (selected options) in multiselect */
        .stMultiSelect div[data-baseweb="multi-select"] span[data-baseweb="select-option"] {
            background-color: #000080 !important; /* Navy blue background */
            color: white !important;  /* White text */
            border-radius: 12px !important;  /* Rounded corners */
            padding: 5px 10px !important;  /* Adjust padding */
        }
        .stMultiSelect div[data-baseweb="multi-select"] span[data-baseweb="select-option"]:hover {
            background-color: #0000cd !important; /* Medium blue on hover */
        }
    </style>
""", unsafe_allow_html=True)

# Example usage of the multiselect widget
selected_sections = st.multiselect(
    "Customize which sections to display. Refresh the page for a full view.",
    options=SECTIONS.keys(),
    default=st.session_state["selected_sections"]
)

render_section_separator()

# **Render Sections Conditionally**
for section_name, module in SECTIONS.items():
    if section_name in selected_sections:
        module.render()
        render_section_separator()
