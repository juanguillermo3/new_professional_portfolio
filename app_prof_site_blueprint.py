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
linkedin_profile = os.getenv("LINKEDIN_PROFILE")

# Default WhatsApp number, which can be overridden by the .env file
whatsapp_number = os.getenv("WHATSAPP_NUMBER", "+57 3053658650")


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
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

