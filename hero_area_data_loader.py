import streamlit as st
import os
import json
from dotenv import load_dotenv
from exceptional_ui import (
    html_for_tooltip_from_large_list,
    setup_tooltip_behavior
)
from front_end_utils import render_section_separator
import hashlib
import datetime

# Load environment variables
load_dotenv()

# Retrieve the mock prefix from the environment, defaulting to "[MOCK TOOLTIP]" if not set
MOCK_INFO_PREFIX = os.getenv("MOCK_INFO", "[MOCK INFO]")

#
# (0)
#
def load_avatar_caption():
    return "God told me I could either be good-looking or an excellent worker."
#
# (1)
#
def load_quote():
    return [
        "My recurring effort has been the <b>modernization of data analysis</b> "  
        "through cutting-edge techniques, such as flexible statistical inference powered by <b>Machine Learning</b>, "  
        "streamlining <em>core business</em> workflows through <b>software development</b> and <b>algorithmic automation</b>, "
        "handling <em>enterprise-grade datasets</em> with <b>modern data technology</b>, "  
        "grouping data by <em>meaning</em> with <b>Natural Language Processing</b>, "  
        "and enabling dynamically <em>decision-making</em> through the <b>agency of Large Language Models.</b> "
    ]
#
# (2)
#
def load_code_samples():
    return [
        {"title": "🚀 Genetic Algorithms for forecasting app sales", "url": "https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz"},
        {"title": "🧩 Ensemble Learning for automated hiring in Human Resources", "url": "https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvAO"}
    ]
#
# (3)
#
def load_detailed_offerings():
    offerings = [
        {
            "title": "⚡ 1. High-Performance Prediction of Key Business Outcomes",
            "description": "I implement <em>statistically driven inference</em> of predictive patterns powered by <em>Machine Learning</em> "
                           "and <em>Deep Learning</em> algorithms. Applications range from forecasting "
                           "the macroeconomic/financial environment to <em>fine-grained predictions</em> from business micro-data (sales forecasting, churn modeling, engagement models).",
            "skills": [
                "Familiarity with predictive algorithms for regression, classification, and forecasting problems.", 
                "Strong grasp of Linear Regression.", 
                "Deep understanding of Machine Learning algorithms for detecting predictive patterns.", 
                "Mastery of the statistical learning workflow for implementing and calibrating predictive models.", 
                "Expert in the development of search and optimization techniques to discover better predictive models."
            ]
        },
        {
            "title": "🔌 2. Sharing Actionable Insights Through Software and Application Development",
            "description": "I develop software applications (batch scripts, APIs, dashboards, web applications) to distribute insights "
                           "and predictions across corporate environments.",
            "skills": [
                "Strong grasp of software engineering best practices.", 
                "Familiarity with software engineering methodologies, architectural models, and design patterns.", 
                "Expertise in developing code using Object-Oriented, Functional, and Asynchronous programming styles.", 
                "Efficient at learning and utilizing new libraries for application development."
            ]
        },
        {
            "title": "🧩 3. Forging Key Datasets from Primary Sources",
            "description": 'As my former boss '
                           '<a href="https://www.linkedin.com/in/susana-mart%C3%ADnez-restrepo-ph-d-1314b137/" target="_blank" style="color: #0073b1; text-decoration: none;">'
                           'Susana Martinez Restrepo</a> said, <em>I can perform data miracles.</em> '
                           'This refers to my ability to clean and organize datasets from complex, multi-source environments '
                           'for research and model development.',
            "skills": [
                "Activate implicit datasets by ETL effort from enterprise systems",
                "Flexible information processing using text-minning, regex, Natural-Language-Processing",
                "Familiarity with algorithms for alternative/unstructured data sources (NLP, GIS, Network Data)",
                "Expertise developing complex merges from multiple data sources"
            ]
        },
        {
            "title": "🛠️ 4. Fast Learning of Modern Data Stacks",
            "description": "I integrate tools and technologies for modern data analysis, committing to research the "
                           "unique purposes of each tool and efficiently write workflows around them using GPT.",
            "subitems": [
                "<strong>Excellence Tier (I know the code line by heart):</strong> Python, R Studio, Stata, GPT",
                "<strong>Proficiency Tier:</strong> Airflow, SQL, Spark, Bash scripting",
                "<strong>Currently Learning:</strong> Docker, Kubernetes, GitHub, Big Data Cloud tools, SQLAlchemy, Django"
            ],
            "skills": [
                "Expert use of Python, R Studio and Stata for applied statistical analysis.",
                "Proficient implementation of Object-Oriented programming in Python (Core Features, OOP), Functional Programming in R (dplyr, ggplot, shiny, regex).",
                "Proficient implementation of analytical queries using SQL.",
                "Proficient implementation of distributed computing (PySpark) and workflow orchestration (Airflow).",
                "Expertise developing and maintaining code in AI-accelerated environments (GPT and Copilot).",
                "Fast pace of research/assimilation of new tools."
            ]
        },
        {
            "title": "🛸 5. Unpacking Artificial Intelligence for Data Analysis",
            "description": "I prepare myself by means of self-learning for the disruption of Artificial Intelligence in software development and the rise of LLM-powered applications."
        },
        {
            "title": "⚖️ (Bonus) Rigorous Economic Mindset",
            "description": "As a professional economist, I over-simplify complex social phenomena by casually referencing supply and demand (kidding!). "
                           "But really, I approach data analysis with a focus on causal reasoning, marginal effects, and counterfactual analysis."
        }
    ]
    return offerings


def custom_html_for_offerings(id_pattern="offering-{}", colors=["#f0f0f0", "#ffffff"]):

    
    import streamlit as st
    
    offerings = load_detailed_offerings()
    
    # 🔹 Hardcoded styles using `st.markdown`
    style_block = """
    <style>
        .test-trigger:hover ~ .test-hover {
            display: inline;
            color: red;
            font-weight: bold;
        }
        .title-test:hover ~ .hoover-test {
            display: inline;
            color: blue;
            font-weight: bold;
        }
    </style>
    """
    
    st.markdown(style_block, unsafe_allow_html=True)  # Explicitly inject styles
    
    # 🔹 Offerings HTML
    offering_html = '<h3 class="offerings-title">Key Professional Offerings</h3>'
    offering_html += '<ul style="list-style-type: none;">'  # Removes bullet points
    
    for i, offer in enumerate(offerings):
        element_id = f"offer-{i+1}"
        
        # Main offering item
        offering_html += f'<li style="padding: 8px; border-radius: 4px; margin-bottom: 10px;">'
        offering_html += f'<p><strong class="title-{element_id}" style="cursor: pointer;">{offer["title"]}</strong></p>'
        offering_html += f'<span class="hoover-{element_id}" style="display: none;">{offer["description"]}</span>'
        
        # 🔹 Explicit hover rule in `st.markdown`
        style_rule = f"""
        <style>
            .title-{element_id}:hover ~ .hoover-{element_id} {{
                display: inline;
                color: green;
                font-weight: bold;
            }}
        </style>
        """
        st.markdown(style_rule, unsafe_allow_html=True)  # Inject per-item style
    
        offering_html += '</li>'
    
    offering_html += '</ul>'
    
    # 🔹 Add Hardcoded Debugging Test Case at the End
    offering_html += """
        <p class="test-trigger" style="cursor: pointer;">Hover over me!</p>
        <span class="test-hover" style="display: none;">This should appear!</span>
    """
    
    # Display the final HTML
    st.markdown(offering_html, unsafe_allow_html=True)
    return "", ""

    














