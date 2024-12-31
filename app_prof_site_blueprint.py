import streamlit as st
import random
import os
import re

# Default WhatsApp number, which can be overridden by the .env file
whatsapp_number = os.getenv("WHATSAPP_NUMBER", "+57 3053658650")
# Set the title of the app
st.set_page_config(page_title="Welcome to My Professional Portfolio", layout="centered")

# Title Section
st.title("Welcome to My Professional Portfolio")
st.write("Explore the recommendations and learn more about my professional background.")


# Number of recommended items and columns
NUM_RECOMMENDED_ITEMS = 6
NUM_COLUMNS = 3

# Flattened structure for the recommendations
def generate_recommendations():
    return [
        {"project": "Ethology Research", "image": "https://via.placeholder.com/150", "title": "Ethology Data Collection", "description": "Module on data collection techniques."},
        {"project": "Ethology Research", "image": "https://via.placeholder.com/150", "title": "Behavioral Data Analysis", "description": "Analyzing animal behavior in the wild."},
        {"project": "Forecasting Sales with Artificial Intelligence", "image": "https://via.placeholder.com/150", "title": "Sales Forecasting with ML", "description": "Using machine learning models for accurate sales predictions."},
        {"project": "Forecasting Sales with Artificial Intelligence", "image": "https://via.placeholder.com/150", "title": "AI in Retail", "description": "Application of AI techniques in retail sales forecasting."},
        {"project": "Ensemble Models for Human Resources", "image": "https://via.placeholder.com/150", "title": "HR Data Analysis", "description": "Leveraging ensemble models for employee retention."},
        {"project": "Ensemble Models for Human Resources", "image": "https://via.placeholder.com/150", "title": "Predicting Employee Turnover", "description": "Predictive modeling for employee turnover using ensemble techniques."},
        {"project": "Trends in the Colombian Labor Market", "image": "https://via.placeholder.com/150", "title": "Labor Market Trends Analysis", "description": "Analyzing the evolution of the Colombian labor market."},
        {"project": "Trends in the Colombian Labor Market", "image": "https://via.placeholder.com/150", "title": "Job Market Forecasting", "description": "Predicting future job trends in Colombia using data analytics."},
    ]

# Streamlit Title and Subheader
st.title("Recommendation System")
st.subheader("Discover content tailored to your needs")

# Query Input
query = st.text_input(
    "Search for recommendations by keyword (e.g., Python, R):", 
    placeholder="Type a keyword and press Enter"
)

# Radial Button for Project Filter
projects = ["All Projects"] + list({rec["project"] for rec in generate_recommendations()})
selected_project = st.radio("Filter recommendations by project:", projects)

# Container for Recommendations
st.markdown("---")
recsys_area = st.container()

with recsys_area:
    # Get recommendations
    recommendations = generate_recommendations()
    
    # Apply project filter
    if selected_project != "All Projects":
        recommendations = [rec for rec in recommendations if rec["project"] == selected_project]
    
    # Apply query filter
    if query:
        query_pattern = re.compile(re.escape(query), re.IGNORECASE)
        recommendations = [
            rec for rec in recommendations 
            if query_pattern.search(rec["title"]) or query_pattern.search(rec["description"])
        ]

    # Limit the number of recommendations
    recommendations = recommendations[:NUM_RECOMMENDED_ITEMS]

    # Display recommendations
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

# Add some space between the recsys and next section
st.markdown("<br>", unsafe_allow_html=True)

# **Services Section** - No query, fixed content
st.subheader("Services I Offer 💼")
st.markdown('<p style="color: gray;">Here are the key services I provide to my clients. Hover over the titles for more information.</p>', unsafe_allow_html=True)
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
st.subheader("About Me 👤")
#st.tooltip("Learn more about my professional background and expertise.")
st.write("Here's a little bit about me:")

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
st.subheader("Connect with Me 📱")
#st.tooltip("Feel free to connect with me via social media or WhatsApp.")
st.write("You can reach me on the following platforms:")

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
