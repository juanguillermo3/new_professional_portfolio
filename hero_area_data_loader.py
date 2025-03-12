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


#def load_detailed_offering(id_pattern="offering-{}", colors=["#f0f0f0", "#ffee00"]):
def load_detailed_offering(id_pattern="offering-{}", colors=["#f0f0f0", "#ffffff"]):
    offerings = [
        {
            "title": "Inferential Statistics & High-Performance Predictive Analytics",
            "description": "I research and implement techniques for regression, classification, and forecasting use cases, \
            with applications ranging from macroeconomic and financial forecasting to microdata predictions in various systems.",
            "skills": [
                "Strong understanding of linear regression. ", 
                "Strong understanding of Machine Learning algorithm for pattern detection. ", 
                "Strong grips on the developmen cycle of predictive models for regression, classification and forecasting. ", 
                "Expertise developing search and optimization algorithms to discover best models. " 
            ]
        },
        {
            "title": "Software & Application Development for Inference Distribution",
            "description": "I develop applications (batch scripts, APIs, dashboards, web applications) to distribute insights \
            and predictions across corporate environments.",
            "skills": [
                "Strong understanding of software engineering. ", 
                "Familiarity witg software engineering methodologies, architectural and design patterns. ", 
                "Expertise with development of code using Object Oriented, Functional and Asyncrhonous styles. ", 
                "High adaptability to using key libraries for application development. ",  
            ]
        },
        {
            "title": "Data Engineering",
            "description": "As my former boss Susana Martinez Restrepo said, 'I can perform data miracles.' This refers to my \
            ability to clean and organize datasets from complex, multi-source environments for research and model development.",
            "skills": [
                "Facility to engage with structured and unstructured sources . ", 
                "Foundations on NLP, GIS, and network analysis. ",  
                "High expertise designing advanced merges and data sources. ", 
                "Expertise using text-minning and NLP for information processing . ", 
            ]
        },
        {
            "title": "Holistic Understanding of Modern Tooling",
            "description": "I integrate tools and technologies for modern data analysis, committing to research the \
            unique purposes of each tool and efficiently write workflows around them using GPT.",
            "skills": ["Cloud Computing", "Containerization"],
            "subitems": [
                "<strong>Excellence Tier (I know the code line by heart):</strong> Python, R Studio, Stata, GPT",
                "<strong>Proficiency Tier:</strong> Airflow, SQL, Spark, Bash scripting",
                "<strong>Currently Learning:</strong> Docker, Kubernetes, GitHub, Big Data Cloud tools, SQLAlchemy, Django"
            ]
        },
        {
            "title": "Research effort on AI & LLM powered applications",
            "description": "I prepare myself by means of self-learning for the disruption of Artificial Intelligence in software development and the rise of LLM-powered applications.",
            "skills": ["Prompt Engineering", "Fine-Tuning LLMs"]
        },
        {
            "title": "Bonus: Rigorous Economic Mindset",
            "description": "As a professional economist, I over-simplify complex social phenomena by casually referencing supply and demand (kidding!).  \
            But really, I approach data analysis with a focus on causal reasoning, marginal effects, and counterfactual analysis.",
            "skills": ["Causal Inference", "Time Series Analysis"]
        }
    ]

    # Initialize HTML output
    offering_html = '<h3>(5+1) Key Differentials of My Professional Offering</h3>'
    offering_html += '<ol style="padding-left: 20px;">'
    
    # Collect element IDs for tooltips
    tooltip_elements = []
    
    # Generate offering list
    for i, offer in enumerate(offerings):
        element_id = id_pattern.format(i+1)
        bg_color = colors[i % len(colors)]
        offering_html += f'<li id="{element_id}" style="background-color: {bg_color}; padding: 8px; border-radius: 4px;">'
        offering_html += f'<strong>{i+1}. {offer["title"]}</strong>: {offer["description"]}'

        if "subitems" in offer:
            offering_html += '<ul style="list-style-type: none; padding-left: 0;">'
            for subitem in offer["subitems"]:
                offering_html += f'<li>{subitem}</li>'
            offering_html += '</ul>'

        # Insert the tooltip for the list of technical skills
        if "skills" in offer:
            offering_html += html_for_tooltip_from_large_list(offer["skills"], label="Technical Skills", element_id=element_id, color="#555", emoji="🏅")
            tooltip_elements.append(element_id)  # Store the ID for hover logic

        offering_html += '</li>'
    
    offering_html += '</ol>'
    
    # Include tooltip styling once
    st.markdown(install_tooltip_styling(),unsafe_allow_html=True)
    
    # Add tooltip hover logic for all elements
    for element_id in tooltip_elements:
        st.markdown(install_tooltip_triggering_logic(element_id),unsafe_allow_html=True)
    
    return offering_html

