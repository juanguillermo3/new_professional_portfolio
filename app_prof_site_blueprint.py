"""
project: new_professional_portfolio
title: Web Application
description: Streamlit based Front-End application for my professional portfolio. 
Author: Juan Guillermo
field: something

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

# Load environment variables
load_dotenv(override=True)

# Environment configurations
ENVIRONMENT = os.getenv("ENVIRONMENT")
REPO_OWNER = os.getenv("REPO_OWNER")
LINKEDIN_PROFILE = os.getenv("LINKEDIN_PROFILE")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")

# Define available sections for customization
SECTIONS = {
    "About this portfolio": about,
    "RecSys": recsys,
    "Services": services,
    "About Me": cv,
    "Connect with Me": socials
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

st.title("Welcome to My Professional Site")

# **Hero Section (Always Rendered)**
hero.render()
render_section_separator()

# **Customization Options**
if "selected_sections" not in st.session_state:
    st.session_state["selected_sections"] = list(SECTIONS.keys())

# UI Elements for Section Selection
selected_sections = st.multiselect(
    "Personalize which sections of this portfolio are visible.",
    options=SECTIONS.keys(),
    default=st.session_state["selected_sections"],
    format_func=lambda x: x  # Ensure full label visibility
)

if st.button("Select All", use_container_width=True):
    selected_sections = list(SECTIONS.keys())  # Activate all sections

# Update session state to store selections
st.session_state["selected_sections"] = selected_sections

# **Render Sections Conditionally**
for section_name, module in SECTIONS.items():
    if section_name in selected_sections:
        module.render()
        render_section_separator()



