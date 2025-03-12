import streamlit as st
import os
import json
from dotenv import load_dotenv
from exceptional_ui import (
    html_for_tooltip_from_large_list,
    install_tooltip_styling,
    install_tooltip_triggering_logic
)

# Load environment variables
load_dotenv()

# Retrieve the mock prefix from the environment, defaulting to "[MOCK TOOLTIP]" if not set
MOCK_INFO_PREFIX = os.getenv("MOCK_INFO", "[MOCK INFO]")

def load_quote():
    return [
        "<b>Modern data analysis</b> requires engaging with and developing <b>substantial software</b>, "  
        "such as <b>data gathering, processing, and visualization applications</b>. "  
        "Moreover, <b>software automation</b> is key for <b>distributing inferences</b> from <b>statistical analysis</b>, "  
        "whether derived from <b>econometric models</b> or <b>machine learning predictions</b>. "  
        "Bottom line: I recognize the deep connection between <b>data analysis</b> and <b>software development</b>, "  
        "hence my effort to <b>serve them within a unified framework</b>." ,
            
        "I am Juan Guillermo, a professional economist. "  
        "I have built my career developing data analysis and software application scripts "  
        "for research and operational environments. "  
        "My business is discovering the more <b>powerful abstractions</b> to <b>effectively work with data</b>, "  
        "implementing them with <b>software engineering standards</b> to <b>build up data-driven intelligence</b> "  
        "for key corporate and social systems. "  
        "My broader professional vision interconnects all the technologies essential for modern data analysis—"  
        "spanning <b>data mining</b>, <b>artificial intelligence models</b>, <b>algorithms</b>, <b>software engineering workflows</b>, "  
        "and <b>information tools</b>—into a cohesive and holistic framework."  

    ]

def load_avatar_caption():
    return "God told me I could either be good-looking or an excellent worker."

def load_code_samples():
    return [
        {"title": "🚀 Genetic Algorithms for forecasting app sales", "url": "https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz"},
        {"title": "🧩 Ensemble Learning for automated hiring in Human Resources", "url": "https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvAO"}
    ]


import hashlib
import datetime

import hashlib
import datetime
import streamlit as st

def load_detailed_offering(id_pattern="offering-{}", colors=["#f0f0f0", "#ffffff"]):
    # Generate a hash from the system date
    system_date = datetime.datetime.now().strftime("%Y-%m-%d")
    style_prefix = hashlib.md5(system_date.encode()).hexdigest()[:8]  # Shorten hash for readability

    offerings = [
        {
            "title": "Inferential Statistics & High-Performance Predictive Analytics",
            "description": "I research and implement techniques for regression, classification, and forecasting use cases, \
            with applications ranging from macroeconomic and financial forecasting to microdata predictions in various systems.",
            "skills": [
                "Strong understanding of linear regression.", 
                "Strong understanding of Machine Learning algorithms for pattern detection.", 
                "Strong grips on the development cycle of predictive models for regression, classification, and forecasting.", 
                "Expertise developing search and optimization algorithms to discover best models." 
            ]
        },
        {
            "title": "Software & Application Development for Inference Distribution",
            "description": "I develop applications (batch scripts, APIs, dashboards, web applications) to distribute insights \
            and predictions across corporate environments.",
            "skills": [
                "Strong understanding of software engineering.", 
                "Familiarity with software engineering methodologies, architectural and design patterns.", 
                "Expertise with development of code using Object-Oriented, Functional, and Asynchronous styles.", 
                "High adaptability to using key libraries for application development."  
            ]
        }
    ]

    # Initialize session state variables safely
    if "installed_tooltips" not in st.session_state:
        st.session_state["installed_tooltips"] = set()
    
    if "tooltip_style_installed" not in st.session_state:
        st.session_state["tooltip_style_installed"] = False
    
    # Initialize HTML output
    offering_html = '<h3>(5+1) Key Differentials of My Professional Offering</h3>'
    offering_html += '<ol style="padding-left: 20px;">'

    # Generate offering list
    for i, offer in enumerate(offerings):
        element_id = id_pattern.format(i+1)
        bg_color = colors[i % len(colors)]
        offering_html += f'<li id="{element_id}" style="background-color: {bg_color}; padding: 8px; border-radius: 4px;">'
        offering_html += f'<strong>{i+1}. {offer["title"]}</strong>: {offer["description"]}'

        # Insert tooltip for technical skills (only if not installed before)
        if "skills" in offer and element_id not in st.session_state["installed_tooltips"]:
            tooltip_html = html_for_tooltip_from_large_list(
                offer["skills"], label="Technical Skills", element_id=element_id, color="#555", emoji="🏅"
            )
            offering_html += tooltip_html
            st.session_state["installed_tooltips"].add(element_id)  # Mark as installed

        offering_html += '</li>'
    
    offering_html += '</ol>'
    
    # Install tooltip styling once
    if not st.session_state["tooltip_style_installed"]:
        st.markdown(install_tooltip_styling(), unsafe_allow_html=True)
        st.session_state["tooltip_style_installed"] = True
    
    # Apply tooltip logic dynamically only for new tooltips
    for element_id in st.session_state["installed_tooltips"]:
        st.markdown(install_tooltip_triggering_logic(element_id), unsafe_allow_html=True)

    return offering_html


