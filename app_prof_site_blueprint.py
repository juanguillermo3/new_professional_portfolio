import streamlit as st
import random
import os
import re

# Default WhatsApp number, which can be overridden by the .env file
whatsapp_number = os.getenv("WHATSAPP_NUMBER", "+57 3053658650")

# Set the title of the app
st.set_page_config(page_title="Welcome to My Professional Portfolio", layout="centered")

# **Title Section**
st.title("Welcome to My Professional Portfolio")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p style="color: gray;">Explore the recommendations and learn more about my professional background.</p>', unsafe_allow_html=True)

# Horizontal rule
st.markdown("---")

# **Recommendation System Section**
st.subheader("Recommendation System")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p style="color: gray;">Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category.</p>', unsafe_allow_html=True)

# Horizontal rule
st.markdown("---")

# Query Input
query = st.text_input(
    "Search for recommendations by keyword (e.g., Python, R):", 
    placeholder="Type a keyword and press Enter"
)

# Radial Button for Project Filter
projects = ["All Projects"] + list({rec["project"] for rec in generate_recommendations()})
selected_project = st.radio("Filter recommendations by project:", projects)

# Container for Recommendations
recsys_area = st.container()
with recsys_area:
    recommendations = generate_recommendations()
    if selected_project != "All Projects":
        recommendations = [rec for rec in recommendations if rec["project"] == selected_project]
    if query:
        query_pattern = re.compile(re.escape(query), re.IGNORECASE)
        recommendations = [
            rec for rec in recommendations 
            if query_pattern.search(rec["title"]) or query_pattern.search(rec["description"])
        ]
    recommendations = recommendations[:NUM_RECOMMENDED_ITEMS]
    for i in range(0, len(recommendations), NUM_COLUMNS):
        cols = st.columns(NUM_COLUMNS)
        for col, rec in zip(cols, recommendations[i:i + NUM_COLUMNS]):
            with col:
                st.markdown(f"""
                    <div style="border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); padding: 10px; text-align: center;">
                        <img src="{rec['image']}" alt="{rec['title']}" style="border-radius: 10px; width: 100%; height: auto;">
                        <h5>{rec['title']}</h5>
                        <p>{rec['description']}</p>
                    </div>
                """, unsafe_allow_html=True)

# **Services Section**
st.subheader("Services I Offer 💼")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p style="color: gray;">Here are the key services I provide to my clients. Hover over the titles for more information.</p>', unsafe_allow_html=True)

# Horizontal rule
st.markdown("---")

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

# **About Me Section**
st.subheader("About Me 👤")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p style="color: gray;">Learn more about my professional background and expertise. Below are key differentiators in my professional offering.</p>', unsafe_allow_html=True)

# Horizontal rule
st.markdown("---")

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

# **Connect with Me Section**
st.subheader("Connect with Me 📱")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p style="color: gray;">Feel free to connect with me via social media or WhatsApp.</p>', unsafe_allow_html=True)

# Horizontal rule
st.markdown("---")

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
