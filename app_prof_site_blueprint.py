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
from professional_bio import bio_component
from dotenv import load_dotenv, dotenv_values
from front_end_utils import render_section_separator
from hero_area import hero
from rec_sys import recsys


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
linkedin_profile = os.getenv("LINKEDIN_PROFILE")


#
# **Hero Section**

#
hero.render()
# 
render_section_separator()

#
# **About this portfolio**
#

st.subheader("About this portfolio")
st.markdown("---")
st.markdown(f'<p style="color: gray;">{
    "In addition of holding the new version of my professional portfolio, this project showcases development in a project to apply emergent tecnologies to create practical solutions to workers struggles in the laboral market."
    }</p>', unsafe_allow_html=True)

#
# **System messages/house keeping**
#


if linkedin_profile:
    portfolio_content = f"""
    <style>
    .emoji {{
        font-size: 1.2em;
    }}
    .message {{
        font-size: 0.95em;  /* Smaller font size */
        line-height: 1.6;
        color: #333;
        text-align: justify;  /* Justified text */
        margin-top: 15px;
        margin-left: 2em;  /* Indentation */
    }}
    .emoji-line {{
        font-size: 1.2em;
        margin-top: 5px;
        margin-left: 2em;
        text-align: justify;
    }}
    </style>
    
    <div class="message">
        <span class="emoji">🔨</span> This portfolio is under development, and you can read the related research in my LinkedIn profile 
        <a href="{linkedin_profile}" target="_blank">here</a>.
    </div>
    
    <div class="message">
        <span class="emoji">⚠️</span> Some of the content in this portfolio is mocked-up by AI.
    </div>
    """
else:
    portfolio_content = "LinkedIn profile not found."

# Render the portfolio content
st.markdown(portfolio_content, unsafe_allow_html=True)

# 
render_section_separator()

#
# **RecSys**
#
    
recsys.render()

# 
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# **Services Section**
st.subheader("Services Lines 🛠️")
st.markdown("---")
st.markdown('<p style="color: gray;">Here are the key services I provide to my clients. Hover over the titles for more information.</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

services_area = st.container()
with services_area:
    service_cols = st.columns(3)
    services = [
        {"image": "https://via.placeholder.com/150", "title": "Consulting", "description": "Expert advice to help you grow your business."},
        {"image": "https://via.placeholder.com/150", "title": "Data Analysis", "description": "In-depth analysis of your business data to drive decisions."},
        {"image": "https://via.placeholder.com/150", "title": "Software Development", "description": "Building robust and scalable software solutions."},
    ]
    for i, service in enumerate(services):
        with service_cols[i % 3]:
            st.markdown(f"""
                <div style="border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); padding: 10px; text-align: center;">
                    <img src="{service['image']}" alt="{service['title']}" style="border-radius: 10px; width: 100%; height: auto;">
                    <h5>{service['title']}</h5>
                    <p>{service['description']}</p>
                </div>
            """, unsafe_allow_html=True)

# 
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# **About Me Section**
st.subheader("About Me 🧑‍💻")
st.markdown("---")
st.markdown('<p style="color: gray;">Learn more about my professional background and expertise. Below are key differentiators in my professional offering.</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

bio_component.render_layout()

key_differentials = [
    "Expertise in data-driven decision-making.",
    "Passion for delivering scalable and efficient software solutions.",
    "Proven track record in consulting across diverse industries.",
    "Strong background in research and development.",
    "Dedicated to continuous learning and skill enhancement.",
]
st.markdown("<ol>", unsafe_allow_html=True)
for item in key_differentials:
    st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
st.markdown("</ol>", unsafe_allow_html=True)

# 
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# **Connect with Me Section**
st.subheader("Connect with Me 🤝")
st.markdown("---")
st.markdown('<p style="color: gray;">Feel free to connect with me via social media or WhatsApp.</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


#import streamlit as st

class SocialMediaButtons:
    def __init__(self, links: dict):
        self.links = links
        # Define colors for each platform
        self.platform_colors = {
            "WhatsApp": "#25D366",
            "LinkedIn": "#0077B5",
            "GitHub": "#333333",
            "Facebook": "#3b5998"
        }

    def create_button(self, platform, url):
        color = self.platform_colors.get(platform, "#000000")  # Default to black if not found
        return f"""
            <a href="{url}" target="_blank">
                <button style="background-color:{color}; color:white; border-radius:10px; 
                               padding:10px 20px; font-size:16px; border:none; margin: 5px;">
                    {platform}
                </button>
            </a>
        """

    def render_buttons(self):
        # Create a container for the social media buttons
        buttons_area = st.container()

        with buttons_area:
            # Use a flex container for layout and keep the buttons well-spaced
            st.markdown('<div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 10px;">', unsafe_allow_html=True)

            # Render each button for each platform
            for platform, url in self.links.items():
                button_html = self.create_button(platform, url)
                st.markdown(button_html, unsafe_allow_html=True)

            # Close the flex container
            st.markdown('</div>', unsafe_allow_html=True)

# Example usage:
social_links = {
    "LinkedIn": "https://www.linkedin.com/in/juan-guillermo-osio/",
    "GitHub": "https://github.com/juanguillermo3/",
    "WhatsApp": "https://wa.me/573053658650",
    "Facebook": "https://www.facebook.com/juan.jaramillo.96"
}

# Create an instance of the SocialMediaButtons class and render the buttons
social_buttons = SocialMediaButtons(social_links)
social_buttons.render_buttons()



# 
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

