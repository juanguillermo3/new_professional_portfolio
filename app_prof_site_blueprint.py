"""
project: new_professional_portfolio
title: Web Application for a New Professional Portfolio
description: Streamlit based Front End for my professional portfolio. 
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

from hero_area import hero
from rec_sys import recsys


#
def reload_env(dotenv_path=".env"):
    """
    Reloads the .env file, ensuring all variables are updated.

    Args:
        dotenv_path (str): Path to the .env file.
    """
    # Parse current .env values without loading them into os.environ
    current_env = dotenv_values(dotenv_path)

    # Remove any keys from os.environ that exist in the .env file
    for key in current_env.keys():
        if key in os.environ:
            del os.environ[key]

    # Reload .env file into os.environ
    load_dotenv(dotenv_path, override=True)

# Call this at the top of your Streamlit script
reload_env()

#
ENVIRONMENT = os.getenv("ENVIRONMENT")
REPO_OWNER= os.getenv("REPO_OWNER")
REPOS_IN_PORTFOLIO=os.getenv("REPOS_IN_PORTFOLIO").split(",") 


# Get the LinkedIn profile URL from the environment
linkedin_profile = os.getenv("LINKEDIN_PROFILE")

# Default WhatsApp number, which can be overridden by the .env file
whatsapp_number = os.getenv("WHATSAPP_NUMBER", "+57 3053658650")



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
#
st.title("Welcome to My Professional Portfolio")
# Get the LinkedIn profile URL from the environment
linkedin_profile = os.getenv("LINKEDIN_PROFILE")


hero.render()

# Ensure the profile is available
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
        <span class="emoji">⚠️</span> Some of the content in this portfolio is mocked-up by AI. I hope you can hear my authentic voice in the whole message.
    </div>
    """
else:
    portfolio_content = "LinkedIn profile not found."

# Render the portfolio content
st.markdown(portfolio_content, unsafe_allow_html=True)



# 
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Number of recommended items and columns
NUM_RECOMMENDED_ITEMS = 6
NUM_COLUMNS = 3

# Flattened structure for the recommendations
def generate_recommendations():
    print( metadata_list)
    return [
        {"project": "Ethology Research", "image": "https://via.placeholder.com/150", "title": "Ethology Data Collection", "description": "Module on data collection techniques."},
        {"project": "Ethology Research", "image": "https://via.placeholder.com/150", "title": "Behavioral Data Analysis", "description": "Analyzing animal behavior in the wild."},
        {"project": "Forecasting Sales with Artificial Intelligence", "image": "https://via.placeholder.com/150", "title": "Sales Forecasting with ML", "description": "Using machine learning models for accurate sales predictions."},
        {"project": "Forecasting Sales with Artificial Intelligence", "image": "https://via.placeholder.com/150", "title": "AI in Retail", "description": "Application of AI techniques in retail sales forecasting."},
        {"project": "Ensemble Models for Human Resources", "image": "https://via.placeholder.com/150", "title": "HR Data Analysis", "description": "Leveraging ensemble models for employee retention."},
        {"project": "Ensemble Models for Human Resources", "image": "https://via.placeholder.com/150", "title": "Predicting Employee Turnover", "description": "Predictive modeling for employee turnover using ensemble techniques."},
        {"project": "Trends in the Colombian Labor Market", "image": "https://via.placeholder.com/150", "title": "Labor Market Trends Analysis", "description": "Analyzing the evolution of the Colombian labor market."},
        {"project": "Trends in the Colombian Labor Market", "image": "https://via.placeholder.com/150", "title": "Job Market Forecasting", "description": "Predicting future job trends in Colombia using data analytics."},
    ] + metadata_list
    
# **Recommendation System Section**

st.subheader("Recommendation System 🎯")
st.markdown("---")
st.markdown('<p style="color: gray;">Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category.</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Query Input
query = st.text_input(
    "Search for recommendations by keyword (e.g., Python, R):", 
    placeholder="Type a keyword and press Enter"
)

repos_metadata=load_repos_metadata()
metadata_list=load_modules_metadata()
#st.text(REPOS_IN_PORTFOLIO)
#st.text(metadata_list)


# Radial Button for Project Filter
recommendations = metadata_list
projects = ["All Projects"] + REPOS_IN_PORTFOLIO 
selected_project = st.selectbox("Filter recommendations by project:", projects)


# Container for Recommendations
recsys_area = st.container()

with recsys_area:

    recommendations = metadata_list
    
    # Check if the selected project exists in repos_metadata
    project_metadata = None
    if selected_project != "All Projects":
        for repo in repos_metadata:
            if repo["title"].lower() == selected_project.lower():
                project_metadata = repo
                break

    # Filter recommendations by selected project
    if selected_project != "All Projects":
        recommendations = [rec for rec in recommendations if rec["project"] == selected_project]
    
    # Filter recommendations by search query
    if query:
        query_pattern = re.compile(re.escape(query), re.IGNORECASE)
        recommendations = [
            rec for rec in recommendations 
            if query_pattern.search(rec["title"]) or query_pattern.search(rec["description"])
        ]
    
    # Truncate recommendations to NUM_RECOMMENDED_ITEMS
    recommendations = recommendations[:NUM_RECOMMENDED_ITEMS]
    
    # Add project metadata as the first recommendation (if available)
    if project_metadata:
        project_card = {
            "title": project_metadata["title"],
            "description": project_metadata["description"],
            "url": project_metadata.get("url", None),
            "is_project": True
        }
        recommendations.insert(0, project_card)
    
    # Render recommendations in a grid
    for i in range(0, len(recommendations), NUM_COLUMNS):
        cols = st.columns(NUM_COLUMNS)
        for col, rec in zip(cols, recommendations[i:i + NUM_COLUMNS]):
            with col:
                # Style the project card distinctly
                background_color = "#fff5e6" if rec.get("is_project") else "white"
                border_style = "2px solid gold" if rec.get("is_project") else "1px solid #ddd"
                
                # Render the card
                st.markdown(
                    f"""
                    <div style="background-color: {background_color}; border: {border_style}; 
                                border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                                padding: 10px; text-align: center;">
                        <img src="https://via.placeholder.com/150" alt="{rec['title']}" 
                             style="border-radius: 10px; width: 100%; height: auto;">
                        <h5>{rec['title']}</h5>
                        <p>{rec['description']}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
                
                # Add "See in GitHub" button if URL is present
                if "url" in rec and rec["url"]:
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center; margin-top: 10px;">
                            <a href="{rec['url']}" target="_blank" 
                               style="text-decoration: none;">
                                <button style="background-color: #333; color: white; 
                                               border: none; padding: 10px 20px; 
                                               text-align: center; text-decoration: none; 
                                               font-size: 14px; cursor: pointer; 
                                               border-radius: 5px;">
                                    See in GitHub
                                </button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True
                    )

#recsys.render()

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

