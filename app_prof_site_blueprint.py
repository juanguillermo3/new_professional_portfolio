import streamlit as st
import random
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Default WhatsApp number, which can be overridden by the .env file
whatsapp_number = os.getenv("WHATSAPP_NUMBER", "+57 3053658650")
# Set the title of the app
st.set_page_config(page_title="Welcome to My Professional Portfolio", layout="centered")

# Title Section
st.title("Welcome to My Professional Portfolio")
st.write("Explore the recommendations and learn more about my professional background.")

# Function to generate mock recommendations
def generate_mock_recommendations():
    recommendations = [
        {"image": "https://via.placeholder.com/150", "title": "Project A", "description": "Description of project A."},
        {"image": "https://via.placeholder.com/150", "title": "Project B", "description": "Description of project B."},
        {"image": "https://via.placeholder.com/150", "title": "Project C", "description": "Description of project C."},
        {"image": "https://via.placeholder.com/150", "title": "Project D", "description": "Description of project D."},
        {"image": "https://via.placeholder.com/150", "title": "Project E", "description": "Description of project E."},
        {"image": "https://via.placeholder.com/150", "title": "Project F", "description": "Description of project F."},
    ]
    return random.sample(recommendations, k=3)  # Randomly select k=3 recommendations

# Recsys Query Input (optional for future feature)
query = st.text_input("Ask for a recommendation:", "Type something...")

# **Recommendation Section** - Fixed-size with visual cues
st.subheader("Recommended Content")
st.write("Here are some recommendations based on your query:")

# Add a horizontal line for separation
st.markdown("---")

# Recsys Section with fixed size for recommendations
recsys_area = st.container()

with recsys_area:
    cols = st.columns(3)  # Three columns layout for the cards

    recommendations = generate_mock_recommendations()  # Get recommendations

    # Populate the columns with card components
    for i, rec in enumerate(recommendations):
        with cols[i % 3]:  # Distribute the cards in the 3 columns
            st.markdown(f"""
                <div style="border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); padding: 10px; text-align: center;">
                    <img src="{rec['image']}" alt="{rec['title']}" style="border-radius: 10px; width: 100%; height: auto;">
                    <h5>{rec['title']}</h5>
                    <p>{rec['description']}</p>
                </div>
            """, unsafe_allow_html=True)

# Add some space between the recsys and next section
st.markdown("<br>", unsafe_allow_html=True)

# **Services Section** - No query, fixed content
st.subheader("Services I Offer")
st.write("Below are the services I offer as part of my professional expertise:")

# Add a horizontal line for separation
st.markdown("---")

# Services Section with fixed content
services_area = st.container()

with services_area:
    service_cols = st.columns(3)  # Three columns layout for the services cards

    # Fixed content for services (these are mock services for demonstration)
    services = [
        {"image": "https://via.placeholder.com/150", "title": "Consulting", "description": "Expert advice to help you grow your business."},
        {"image": "https://via.placeholder.com/150", "title": "Data Analysis", "description": "In-depth analysis of your business data to drive decisions."},
        {"image": "https://via.placeholder.com/150", "title": "Software Development", "description": "Building robust and scalable software solutions."},
    ]

    # Populate the columns with service cards
    for i, service in enumerate(services):
        with service_cols[i % 3]:  # Distribute the service cards in 3 columns
            st.markdown(f"""
                <div style="border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); padding: 10px; text-align: center;">
                    <img src="{service['image']}" alt="{service['title']}" style="border-radius: 10px; width: 100%; height: auto;">
                    <h5>{service['title']}</h5>
                    <p>{service['description']}</p>
                </div>
            """, unsafe_allow_html=True)

# Add some space between the services and the next section
st.markdown("<br>", unsafe_allow_html=True)

# **Professional Profile Section**
st.subheader("About Me")

# Ordered List for Key Differentials
st.write("Here are the key differentiators in my professional offering:")

# List of key differentiators (you can modify as per your profile)
key_differentials = [
    "Expertise in data-driven decision-making.",
    "Passion for delivering scalable and efficient software solutions.",
    "Proven track record in consulting across diverse industries.",
    "Strong background in research and development.",
    "Dedicated to continuous learning and skill enhancement.",
]

# Render the ordered list
st.markdown("<ol>", unsafe_allow_html=True)
for item in key_differentials:
    st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
st.markdown("</ol>", unsafe_allow_html=True)


# **Social Media Links and WhatsApp Button**
st.subheader("Connect with Me")

# Social Media Links (example links, customize them with your actual URLs)
social_links = {
    "LinkedIn": "https://www.linkedin.com/in/your-profile/",
    "Twitter": "https://twitter.com/your-profile/",
    "GitHub": "https://github.com/your-profile/",
}

# Display Social Media Links
for platform, url in social_links.items():
    st.markdown(f"[{platform}]({url})")

# Add some space before the WhatsApp button
st.markdown("<br>", unsafe_allow_html=True)

# WhatsApp Button
whatsapp_url = f"https://wa.me/{whatsapp_number}?text=Hello! I'd like to connect with you."
st.markdown(f"""
    <a href="{whatsapp_url}" target="_blank">
        <button style="background-color:#25D366; color:white; border-radius:10px; padding:10px 20px; font-size:16px; border:none;">
            WhatsApp Me
        </button>
    </a>
""", unsafe_allow_html=True)