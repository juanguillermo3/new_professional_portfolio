"""
project: new_professional_portfolio
title: Web Application
description: Streamlit based Front-End application for my professional portfolio. 
Author: Juan Guillermo
field: something

"""

import streamlit as st
import random
import os
import re
from git_api_utils import load_repos_metadata, load_modules_metadata, REPOS_IN_PORTFOLIO
from professional_bio import cv
from dotenv import load_dotenv, dotenv_values
from front_end_utils import render_section_separator
from hero_area import hero
from rec_sys import recsys
from about_section import about
from services_section import services
from socials_section import socials

#
load_dotenv(override=True)

#
ENVIRONMENT = os.getenv("ENVIRONMENT")
REPO_OWNER= os.getenv("REPO_OWNER")
REPOS_IN_PORTFOLIO=os.getenv("REPOS_IN_PORTFOLIO", "lab_market_trends,monkey_research,new_professional_portfolio").split(",") 


# Get the LinkedIn profile URL from the environment
LINKEDIN_PROFILE = os.getenv("LINKEDIN_PROFILE")
# Default WhatsApp number, which can be overridden by the .env file
WHATSAPP_NUMBER= os.getenv("WHATSAPP_NUMBER")

#
# Fixed Navigation Bar
#
st.markdown("""
    <style>
    .top-nav {
        position: fixed;
        top: 0;
        width: 100%;
        background-color: #f8f9fa;
        z-index: 1000;
        padding: 0.5em 1em;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-around;
    }
    .top-nav a {
        text-decoration: none;
        color: #007BFF;
        font-weight: bold;
        padding: 0.5em;
    }
    .top-nav a:hover {
        color: #0056b3;
    }
    </style>
    <div class="top-nav">
        <a href="#hero-section">Home</a>
        <a href="#about-section">About</a>
        <a href="#recsys-section">Recommendations</a>
        <a href="#services-section">Services</a>
        <a href="#connect-section">Connect</a>
    </div>
    <div style="margin-top: 4em;"></div>
""", unsafe_allow_html=True)

#
# **Title Section**
#
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
#
st.title("Welcome to My Professional Portfolio")
# Get the LinkedIn profile URL from the environment
LINKEDIN_PROFILE = os.getenv("LINKEDIN_PROFILE")


#
# **Hero Section**

#
hero.render()
# 
render_section_separator()

#
# **About this portfolio**
#

#
about.render()
# 
render_section_separator()


#
# **RecSys**
#

#
recsys.render()
# 
render_section_separator()

#
# **Services Section**
#

#
services.render()
# 
render_section_separator()

# **About Me Section**

#
cv.render()
#
render_section_separator()

#
# **Connect with Me Section**
#

socials.render()
#
render_section_separator()
