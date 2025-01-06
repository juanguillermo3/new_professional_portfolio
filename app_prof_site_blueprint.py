import streamlit as st
import random
import os
import re
from git_api import repos_metadata, metadata_list
#from professional_bio import *

# Default WhatsApp number, which can be overridden by the .env file
whatsapp_number = os.getenv("WHATSAPP_NUMBER", "+57 3053658650")

# Set the title of the app
st.set_page_config(page_title="Welcome to My Professional Portfolio", layout="centered")




st.title("Welcome to My Professional Portfolio")

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

#bio_component.render_layout()


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


# Query Input
query = st.text_input(
    "Search for recommendations by keyword (e.g., Python, R):", 
    placeholder="Type a keyword and press Enter"
)

# Radial Button for Project Filter
recommendations = metadata_list
projects = ["All Projects"] + list({rec["project"] for rec in recommendations })
selected_project = st.selectbox("Filter recommendations by project:", projects)


# Container for Recommendations
recsys_area = st.container()

with recsys_area:
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




# 
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# **Services Section**
st.subheader("Services I Offer 🛠️")
st.markdown("---")
st.markdown('<p style="color: gray;">Here are the key services I provide to my clients. Hover over the titles for more information.</p>', unsafe_allow_html=True)

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


social_links = {
    "LinkedIn": "https://www.linkedin.com/in/your-profile/",
    "Twitter": "https://twitter.com/your-profile/",
    "GitHub": "https://github.com/your-profile/",
}
for platform, url in social_links.items():
    st.markdown(f"[{platform}]({url})")

whatsapp_url = f"https://wa.me/{whatsapp_number}?text=Hello! I'd like to connect with you."
st.markdown(f"""
    <a href="{whatsapp_url}" target="_blank">
        <button style="background-color:#25D366; color:white; border-radius:10px; padding:10px 20px; font-size:16px; border:none;">
            WhatsApp Me
        </button>
    </a>
""", unsafe_allow_html=True)

# 
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

