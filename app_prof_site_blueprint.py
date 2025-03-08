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
from front_end_utils import html_for_paragraph_with_expandable_details

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
#display_floating_linkedin_button( linkedin_url=LINKEDIN_PROFILE, horizontal_position= "80%",)
#display_floating_whatsapp_button( whatsapp_number=WHATSAPP_NUMBER, horizontal_position= "65%",)
#close_floating_buttons_container()

st.title("Welcome to My Professional Site")

# **Hero Section (Always Rendered)**
hero.render()
cv.render()
