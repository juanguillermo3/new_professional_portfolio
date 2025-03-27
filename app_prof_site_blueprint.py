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
    "Services": services,
    "Curriculum Vitae": cv,
    "Testimonials": testimonials
}

# fetch desired section from url parameters 
#query_params = st.experimental_get_query_params()
#query_params = st.query_params()

#query_sections = query_params.get("section")

query_sections = [st.query_params["section"]]
if not query_sections or query_sections==["Home"]:
    displayed_sections=list(SECTIONS.keys())
else:
    displayed_sections=query_sections
st.write(query_sections)

# Example usage of the multiselect widget
selected_sections = st.multiselect(
    "Customize which sections to display. Refresh the page for a full view.",
    options=SECTIONS.keys(),
    default=displayed_sections
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


if query_sections==["Home"]:
    st.title("Welcome to My Professional Site")
    hero.render()
    render_section_separator()
    render_section_separator()

# **Render Sections Conditionally**
for section_name, module in SECTIONS.items():
    if section_name in selected_sections:
        module.render()
        render_section_separator()


render_multi_page_navigation()
display_floating_whatsapp_button( whatsapp_number=WHATSAPP_NUMBER, horizontal_position= "65%",)

